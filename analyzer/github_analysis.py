from datetime import datetime, timezone


class GitHubAnalyzer:

    def analyze(self, github_data):
        """
        Analyze GitHub repository signals and return
        structured scoring + textual reasons.
        """

        # If API failed or no repo link
        if github_data is None:
            return {
                "github_score": 2,
                "github_reasons": ["GitHub repository unavailable or not found."]
            }

        score = 0
        reasons = []

        stars = github_data.get("stars", 0)
        forks = github_data.get("forks", 0)
        archived = github_data.get("archived", False)
        last_push = github_data.get("last_push")

        # -------------------------------------------------
        # 1️⃣ Archived repository (strong signal)
        # -------------------------------------------------
        if archived:
            score += 3
            reasons.append("Repository is archived.")

        # -------------------------------------------------
        # 2️⃣ Very low popularity
        # -------------------------------------------------
        if stars < 5:
            score += 2
            reasons.append("Very low GitHub popularity (few stars).")

        # Slight boost if zero forks AND very low stars
        if stars == 0 and forks == 0:
            score += 1
            reasons.append("No community activity (0 stars, 0 forks).")

        # -------------------------------------------------
        # 3️⃣ Repository inactivity check
        # -------------------------------------------------
        if last_push:
            try:
                last_push_date = datetime.strptime(
                    last_push, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)

                now = datetime.now(timezone.utc)
                years_inactive = (now - last_push_date).days / 365

                if years_inactive >= 2:
                    score += 3
                    reasons.append("Repository inactive for over 2 years.")
                elif years_inactive >= 1:
                    score += 1
                    reasons.append("Repository inactive for over 1 year.")

            except Exception:
                # If date parsing fails, do not crash
                pass

        return {
            "github_score": score,
            "github_reasons": reasons
        }