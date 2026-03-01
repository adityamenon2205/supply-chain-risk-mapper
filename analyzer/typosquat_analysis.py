from difflib import SequenceMatcher


class TyposquatAnalyzer:

    def __init__(self):
        # Top popular packages (can expand later)
        self.popular_packages = [
            "requests",
            "flask",
            "django",
            "numpy",
            "pandas",
            "urllib3",
            "pytest",
            "scipy",
            "beautifulsoup4"
        ]

    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def analyze(self, package_name):
        suspicious_matches = []

        for popular in self.popular_packages:
            sim = self.similarity(package_name.lower(), popular.lower())

            # If very similar but not exact match
            if 0.80 < sim < 1.0:
                suspicious_matches.append((popular, sim))

        if suspicious_matches:
            reasons = [
                f"Name similar to popular package '{match[0]}' (similarity {round(match[1],2)})"
                for match in suspicious_matches
            ]

            return {
                "typosquat_score": 3,
                "typosquat_reasons": reasons
            }

        return {
            "typosquat_score": 0,
            "typosquat_reasons": []
        }