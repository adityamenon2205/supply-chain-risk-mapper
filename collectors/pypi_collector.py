import requests


class PyPICollector:

    PYPI_URL = "https://pypi.org/pypi/{}/json"

    def fetch_metadata(self, package_name: str):
        url = self.PYPI_URL.format(package_name)

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "name": data["info"]["name"],
            "version": data["info"]["version"],
            "author": data["info"].get("author"),
            "maintainer": data["info"].get("maintainer"),
            "home_page": data["info"].get("home_page"),
            "project_urls": data["info"].get("project_urls"),
            "releases": list(data["releases"].keys())
        }