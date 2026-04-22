from routes.threat_model import threat_bp
from routes.security import security_bp
from routes.analyze import analyze_bp
from flask import Flask, jsonify, request
import requests
import sqlite3
import uuid
import stripe
import os
from openai import OpenAI

app = Flask(__name__)
app.register_blueprint(analyze_bp)
app.register_blueprint(security_bp)
app.register_blueprint(threat_bp)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
stripe.api_key = os.getenv("STRIPE_API_KEY")

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('api_keys.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT,
            plan TEXT,
            requests_used INTEGER
        )
    ''')

    conn.commit()
    conn.close()

init_db()


# ---------------- CHECK API KEY ----------------
def check_api_key(key):
    conn = sqlite3.connect('api_keys.db')
    cursor = conn.cursor()

    cursor.execute('SELECT plan, requests_used FROM users WHERE api_key=?', (key,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None, "Invalid API key"

    plan, requests_used = row
    limit = 5 if plan == "free" else 1000

    if requests_used >= limit:
        conn.close()
        return None, "API limit reached"

    cursor.execute(
        'UPDATE users SET requests_used = requests_used + 1 WHERE api_key=?',
        (key,)
    )

    conn.commit()
    conn.close()

    return {"plan": plan, "requests_used": requests_used + 1}, None


# ---------------- CREATE KEY ----------------
@app.route('/create-key', methods=['GET'])
def create_key():

    new_key = str(uuid.uuid4())

    conn = sqlite3.connect('api_keys.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO users (api_key, plan, requests_used) VALUES (?, ?, ?)',
        (new_key, 'free', 0)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "api_key": new_key,
        "plan": "free"
    })


# ---------------- EVENTS ----------------
@app.route('/events', methods=['GET'])
def get_events():

    apikey = request.args.get("apikey")

    user, error = check_api_key(apikey)
    if error:
        return jsonify({"error": error}), 403

    url = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4328"

    response = requests.get(url)
    data = response.json()

    events = []

    for e in data.get("events", [])[:5]:

        event = {
            "home": e["strHomeTeam"],
            "away": e["strAwayTeam"],
            "date": e["dateEvent"]
        }

        if user["plan"] == "pro":
            event["league"] = e["strLeague"]

        events.append(event)

    return jsonify({
        "plan": user["plan"],
        "requests_used": user["requests_used"],
        "data": events
    })

@app.route('/upgrade', methods=['GET'])
def upgrade():
    key = request.args.get("apikey")

    conn = sqlite3.connect('api_keys.db')
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE users SET plan="pro" WHERE api_key=?',
        (key,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Upgraded to PRO"})
    

@app.route('/create-checkout', methods=['GET'])
def create_checkout():

    apikey = request.args.get("apikey")

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Pro API Access',
                },
                'unit_amount': 500,
            },
            'quantity': 1,
        }],
        mode='payment',

        # 👇 ТУК ПАЗИМ API KEY
        metadata={
            "apikey": apikey
        },

        success_url='http://127.0.0.1:5000/success',
        cancel_url='http://127.0.0.1:5000/cancel',
    )

    return jsonify({"checkout_url": session.url})

@app.route('/webhook', methods=['POST'])
def stripe_webhook():

    event = stripe.Event.construct_from(
        request.get_json(), stripe.api_key
    )

    # Проверяваме дали е платено
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        apikey = session["metadata"]["apikey"]

        # 👉 Upgrade в базата
        conn = sqlite3.connect('api_keys.db')
        cursor = conn.cursor()

        cursor.execute(
            'UPDATE users SET plan="pro" WHERE api_key=?',
            (apikey,)
        )

        conn.commit()
        conn.close()

    return jsonify({"status": "success"})

# -------- AI SECURITY --------
@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    data = request.json or {}
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
You are a cybersecurity AI assistant.

Analyze the text and classify it:
- prompt injection attempt
- malicious intent
- sensitive data leakage
- safe input

Text:
{text}

Return:
risk_level (low/medium/high)
explanation (short)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        return jsonify({
            "analysis": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------- CODE ANALYSIS --------
@app.route("/analyze-code", methods=["POST"])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get("code", "")

        if not code:
            return jsonify({"error": "No code provided"}), 400

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
Analyze the following code:

{code}

Return:
- issues
- improvements
- explanation
"""
        )

        return jsonify({
            "result": response.output_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)