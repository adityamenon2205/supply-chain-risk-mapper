from extractor.dependency_extractor import DependencyExtractor
from collectors.pypi_collector import PyPICollector
import sys


def main():
    extractor = DependencyExtractor(".")
    deps = extractor.extract()

    collector = PyPICollector()

    for dep in deps:
        package_name = dep["package"]["key"]
        print(f"\nFetching metadata for: {package_name}")

        metadata = collector.fetch_metadata(package_name)

        if metadata:
            print("Author:", metadata["author"])
            print("Maintainer:", metadata["maintainer"])
            print("Latest Version:", metadata["version"])
        else:
            print("Failed to fetch metadata")


if __name__ == "__main__":
    main()