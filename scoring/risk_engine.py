class RiskEngine:

    def calculate_risk(self, maintainer_score, inactivity_years, dependency_count):
        score = 0
        reasons = []

        # Maintainer risk
        if maintainer_score >= 2:
            score += 3
            reasons.append("Maintainer instability detected.")

        # Inactivity risk
        if inactivity_years >= 2:
            score += 3
            reasons.append("Project inactive for over 2 years.")

        # Large dependency surface
        if dependency_count >= 5:
            score += 2
            reasons.append("Large dependency surface increases attack exposure.")

        # Normalize score
        if score >= 6:
            category = "HIGH"
        elif score >= 3:
            category = "MEDIUM"
        else:
            category = "LOW"

        return {
            "score": score,
            "category": category,
            "reasons": reasons
        }