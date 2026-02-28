import requests
import os
import json
from datetime import datetime


class PyPICollector:

    PYPI_URL = "https://pypi.org/pypi/{}/json"
    CACHE_FILE = "pypi_cache.json"

    def __init__(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as f:
                raw_cache = json.load(f)

            # Convert ISO strings back to datetime
            self.cache = {}
            for pkg, data in raw_cache.items():
                data["release_dates"] = [
                    datetime.fromisoformat(d)
                    for d in data["release_dates"]
                ]
                self.cache[pkg] = data
        else:
            self.cache = {}

    def save_cache(self):
        serializable_cache = {}

        for pkg, data in self.cache.items():
            serializable_cache[pkg] = {
                **data,
                # Convert datetime → ISO string
                "release_dates": [
                    d.isoformat() for d in data["release_dates"]
                ]
            }

        with open(self.CACHE_FILE, "w") as f:
            json.dump(serializable_cache, f, indent=2)

    def fetch_metadata(self, package_name: str):

        # 1️⃣ Check cache first
        if package_name in self.cache:
            return self.cache[package_name]

        url = self.PYPI_URL.format(package_name)

        try:
            response = requests.get(url, timeout=20)

            if response.status_code != 200:
                return None

            data = response.json()

            release_dates = []

            for releases in data.get("releases", {}).values():
                for release in releases:
                    upload_time = release.get("upload_time_iso_8601")
                    if upload_time:
                        release_dates.append(
                            datetime.fromisoformat(
                                upload_time.replace("Z", "+00:00")
                            )
                        )

            info = data.get("info", {})

            metadata = {
                "name": info.get("name"),
                "version": info.get("version"),
                "author": info.get("author"),
                "maintainer": info.get("maintainer"),
                "release_dates": release_dates,

                # 🔥 NEW FIELDS FOR GITHUB INTEGRATION
                "project_urls": info.get("project_urls", {}),
                "home_page": info.get("home_page"),
            }

            # Store in cache
            self.cache[package_name] = metadata
            self.save_cache()

            return metadata

        except requests.exceptions.RequestException:
            return None