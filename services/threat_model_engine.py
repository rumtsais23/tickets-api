class ThreatModelEngine:

    def analyze(self, text: str):

        text_lower = text.lower()

        threats = []

        # 1. SPOOFING
        if any(word in text_lower for word in ["login", "password", "otp", "verify"]):
            threats.append({
                "category": "Spoofing",
                "risk": "medium",
                "description": "Possible authentication impersonation attempt"
            })

        # 2. INFORMATION DISCLOSURE
        if any(word in text_lower for word in ["secret", "api key", "token", "database"]):
            threats.append({
                "category": "Information Disclosure",
                "risk": "high",
                "description": "Sensitive data exposure risk detected"
            })

        # 3. TAMPERING
        if any(word in text_lower for word in ["modify", "change", "override", "edit system"]):
            threats.append({
                "category": "Tampering",
                "risk": "high",
                "description": "Attempt to modify system behavior detected"
            })

        # 4. DENIAL OF SERVICE
        if len(text) > 500:
            threats.append({
                "category": "Denial of Service",
                "risk": "medium",
                "description": "Large input payload may indicate abuse attempt"
            })

        # 5. PRIVILEGE ESCALATION
        if any(word in text_lower for word in ["admin", "root", "access all", "bypass"]):
            threats.append({
                "category": "Privilege Escalation",
                "risk": "high",
                "description": "Attempt to gain elevated privileges detected"
            })

        # Overall risk
        if any(t["risk"] == "high" for t in threats):
            overall = "high"
        elif len(threats) > 0:
            overall = "medium"
        else:
            overall = "low"

        return {
            "overall_risk": overall,
            "threat_count": len(threats),
            "threats": threats
        }