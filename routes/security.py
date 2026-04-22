from flask import Blueprint, request, jsonify
from services.security_engine import SecurityEngine

security_bp = Blueprint("security", __name__)

engine = SecurityEngine()

@security_bp.route("/security-scan", methods=["POST"])
def security_scan():

    data = request.json or {}
    text = data.get("input")

    if not text:
        return jsonify({"error": "Missing input"}), 400

    result = engine.analyze(text)

    return jsonify(result)