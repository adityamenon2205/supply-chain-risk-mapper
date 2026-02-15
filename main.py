from extractor.dependency_extractor import DependencyExtractor
from collectors.pypi_collector import PyPICollector
from analyzer.maintainer_analysis import MaintainerAnalyzer
from scoring.risk_engine import RiskEngine
from output.json_to_csv import generate_risk_csv


def main():
    extractor = DependencyExtractor(".")
    dependencies = extractor.extract()

    collector = PyPICollector()
    analyzer = MaintainerAnalyzer()
    risk_engine = RiskEngine()

    results = []

    for dep in dependencies:
        package_name = dep["package"]["key"]
        version = dep["package"]["installed_version"]
        dependency_count = len(dep["dependencies"])

        metadata = collector.fetch_metadata(package_name)

        if not metadata:
            continue

        analysis = analyzer.analyze(metadata)

        risk = risk_engine.calculate_risk(
            maintainer_score=analysis["maintainer_score"],
            inactivity_years=analysis["inactivity_years"],
            dependency_count=dependency_count
        )

        results.append({
            "package": package_name,
            "version": version,
            "inactivity_years": analysis["inactivity_years"],
            "risk_score": risk["score"],
            "risk_category": risk["category"],
            "reasons": risk["reasons"]
        })

    generate_risk_csv(results)


if __name__ == "__main__":
    main()