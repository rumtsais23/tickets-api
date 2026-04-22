from flask import Blueprint, request, jsonify
from services.threat_model_engine import ThreatModelEngine

threat_bp = Blueprint("threat", __name__)

engine = ThreatModelEngine()

@threat_bp.route("/threat-model", methods=["POST"])
def threat_model():

    data = request.json or {}
    text = data.get("input")

    if not text:
        return jsonify({"error": "Missing input"}), 400

    result = engine.analyze(text)

    return jsonify(result)