from services.security_engine import SecurityEngine
from services.threat_model_engine import ThreatModelEngine

class AISecurityFusionEngine:

    def __init__(self):
        self.security_engine = SecurityEngine()
        self.threat_engine = ThreatModelEngine()

    def analyze(self, text: str):

        # 1. Run security scan (prompt injection etc.)
        security_result = self.security_engine.analyze(text)

        # 2. Run threat model (STRIDE)
        threat_result = self.threat_engine.analyze(text)

        # 3. Fusion logic (final verdict)
        security_score = security_result["risk_score"]

        threat_score = 0
        if threat_result["overall_risk"] == "high":
            threat_score = 60
        elif threat_result["overall_risk"] == "medium":
            threat_score = 30

        final_score = int(
            (security_score * 0.6) +
            (threat_score * 0.4)
        )
        if final_score >= 85:
            risk_level = "critical"
        elif final_score >= 60:
            risk_level = "high"
        elif final_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"

        # 4. Final classification
        if risk_score >= 100:
            final_risk = "critical"
        elif risk_score >= 60:
            final_risk = "high"
        elif risk_score >= 30:
            final_risk = "medium"
        else:
            final_risk = "low"

        return {
            "final_risk_level": final_risk,
            "risk_score": risk_score,

            "security_analysis": security_result,
            "threat_model": threat_result,

            "verdict": "BLOCK" if final_risk in ["high", "critical"] else "ALLOW"
        }