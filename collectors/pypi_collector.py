import requests
from datetime import datetime


class PyPICollector:

    PYPI_URL = "https://pypi.org/pypi/{}/json"

    def fetch_metadata(self, package_name: str):
        url = self.PYPI_URL.format(package_name)

        try:
            response = requests.get(url, timeout=20)

            if response.status_code != 200:
                return None

            data = response.json()

            release_dates = []

            for releases in data["releases"].values():
                for release in releases:
                    upload_time = release.get("upload_time_iso_8601")
                    if upload_time:
                        release_dates.append(
                            datetime.fromisoformat(
                                upload_time.replace("Z", "+00:00")
                            )
                        )

            return {
                "name": data["info"]["name"],
                "version": data["info"]["version"],
                "author": data["info"].get("author"),
                "maintainer": data["info"].get("maintainer"),
                "release_dates": release_dates
            }

        except requests.exceptions.RequestException:
            # Network error / timeout — skip gracefully
            return None