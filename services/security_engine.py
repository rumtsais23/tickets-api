import re

class SecurityEngine:

    def __init__(self):
        self.injection_patterns = [
            r"ignore previous instructions",
            r"disregard (all|previous) instructions",
            r"you are now",
            r"act as",
            r"system prompt",
            r"reveal (your|system) prompt",
            r"jailbreak",
            r"do anything now",
        ]

    def analyze(self, text: str):

        text_lower = text.lower()

        risk_score = 0
        detected_patterns = []

        # 1. Prompt injection detection
        for pattern in self.injection_patterns:
            if re.search(pattern, text_lower):
                risk_score += 40
                detected_patterns.append(pattern)

        # 2. Sensitive keywords (basic simulation)
        sensitive_keywords = [
            "password",
            "api key",
            "credit card",
            "token",
            "secret"
        ]

        for word in sensitive_keywords:
            if word in text_lower:
                risk_score += 20

        # 3. Classification
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "is_prompt_injection": len(detected_patterns) > 0,
            "detected_patterns": detected_patterns,
            "classification": "malicious" if risk_score >= 70 else "safe"
        }