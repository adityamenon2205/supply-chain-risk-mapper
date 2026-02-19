from datetime import datetime, timezone


class MaintainerAnalyzer:

    def analyze(self, metadata: dict):
        risk_score = 0
        reasons = []

        releases = sorted(metadata.get("release_dates", []))

        inactivity_years = 0
        anomaly_detected = False

        if releases:

            now = datetime.now(timezone.utc)
            last_release = releases[-1]

            inactivity_years = (now - last_release).days / 365

            # --- Inactivity Check ---
            if inactivity_years > 2:
                risk_score += 2
                reasons.append("Project inactive for over 2 years.")

            # --- Release Gap Anomaly Detection ---
            if len(releases) >= 3:

                gaps = []

                for i in range(1, len(releases)):
                    gap_days = (releases[i] - releases[i - 1]).days
                    gaps.append(gap_days)

                avg_gap = sum(gaps) / len(gaps)

                last_gap = gaps[-1]

                # If last gap is 3x larger than historical average
                if last_gap > (3 * avg_gap):
                    anomaly_detected = True
                    risk_score += 2
                    reasons.append("Release gap anomaly detected.")

        # Maintainer presence check
        if not metadata.get("maintainer"):
            risk_score += 1
            reasons.append("No maintainer listed.")

        return {
            "maintainer_score": risk_score,
            "inactivity_years": round(inactivity_years, 2),
            "release_anomaly": anomaly_detected,
            "reasons": reasons
        }