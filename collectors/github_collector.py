import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubCollector:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")

        # Even if token missing, don't crash entire program
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        } if self.token else {}

    def extract_repo_info(self, github_url):
        try:
            parts = github_url.rstrip("/").split("/")
            owner = parts[-2]
            repo = parts[-1]
            return owner, repo
        except Exception:
            return None, None

    def fetch_repo_data(self, github_url):
        owner, repo = self.extract_repo_info(github_url)

        if not owner or not repo:
            return None

        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        try:
            response = requests.get(
                api_url,
                headers=self.headers,
                timeout=8   # important
            )

            if response.status_code != 200:
                return None

            data = response.json()

            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "archived": data.get("archived", False),
                "last_push": data.get("pushed_at", None),
                "created_at": data.get("created_at", None)
            }

        except requests.exceptions.RequestException:
            # 🔥 Any network failure → just skip GitHub scoring
            return None