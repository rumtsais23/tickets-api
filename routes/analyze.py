from services.fusion_engine import AISecurityFusionEngine
from flask import Blueprint, request, jsonify

analyze_bp = Blueprint("analyze", __name__)
fusion_engine = AISecurityFusionEngine()

@analyze_bp.route("/ai-analyze", methods=["POST"])
def ai_analyze():

    data = request.json or {}
    text = data.get("input", "").strip()

    if not text:
        return jsonify({"error": "Missing input"}), 400

    result = fusion_engine.analyze(text)

    return jsonify(result)