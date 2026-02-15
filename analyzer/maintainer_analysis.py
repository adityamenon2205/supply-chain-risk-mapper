from datetime import datetime, timezone


class MaintainerAnalyzer:

    def analyze(self, metadata: dict):
        risk_score = 0
        reasons = []

        if not metadata.get("maintainer"):
            risk_score += 1
            reasons.append("No maintainer listed.")

        releases = metadata.get("release_dates", [])
        inactivity_years = 0

        if releases:
            last_release = max(releases)

            # FIX: make current time timezone-aware (UTC)
            now = datetime.now(timezone.utc)

            inactivity_years = (now - last_release).days / 365

            if inactivity_years > 2:
                risk_score += 2
                reasons.append("Project inactive for over 2 years.")

        return {
            "maintainer_score": risk_score,
            "inactivity_years": round(inactivity_years, 2),
            "reasons": reasons
        }