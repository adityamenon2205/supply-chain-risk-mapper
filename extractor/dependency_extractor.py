import subprocess
import json
from pathlib import Path


class DependencyExtractor:

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def install_requirements(self):
        """Install requirements.txt inside current environment"""
        req_file = self.project_path / "requirements.txt"

        if not req_file.exists():
            raise FileNotFoundError("requirements.txt not found.")

        subprocess.run(
            ["pip", "install", "-r", str(req_file)],
            check=True
        )

    def get_dependency_tree(self):
        """Return dependency tree as JSON"""
        result = subprocess.run(
            ["pipdeptree", "--json"],
            capture_output=True,
            text=True,
            check=True
        )

        return json.loads(result.stdout)

    def extract(self):
        """Main method to extract dependency data"""
        self.install_requirements()
        return self.get_dependency_tree()