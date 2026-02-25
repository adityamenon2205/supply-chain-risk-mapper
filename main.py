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

    # -------------------------------------------------
    # STEP 1: Register all packages in dependency graph
    # -------------------------------------------------
    for dep in dependencies:
        package_name = dep["package"]["key"]
        dependency_names = [d["key"] for d in dep["dependencies"]]

        risk_engine.add_package(package_name, dependency_names)

    # -------------------------------------------------
    # STEP 2: Compute base risks for all packages
    # -------------------------------------------------
    package_analysis_cache = {}

    for dep in dependencies:
        package_name = dep["package"]["key"]
        version = dep["package"]["installed_version"]
        dependency_count = len(dep["dependencies"])

        metadata = collector.fetch_metadata(package_name)

        if not metadata:
            continue

        analysis = analyzer.analyze(metadata)

        # Calculate base risk and capture reasons
        base_data = risk_engine.calculate_base_risk(
            package_name=package_name,
            maintainer_score=analysis["maintainer_score"],
            inactivity_years=analysis["inactivity_years"],
            dependency_count=dependency_count
        )

        # Store everything for final evaluation
        package_analysis_cache[package_name] = {
            "version": version,
            "analysis": analysis,
            "dependency_count": dependency_count,
            "reasons": base_data["reasons"]
        }

    # -------------------------------------------------
    # STEP 3: Compute final propagated risks
    # -------------------------------------------------
    for package_name, data in package_analysis_cache.items():

        final_risk = risk_engine.calculate_final_risk(package_name)

        results.append({
            "package": package_name,
            "version": data["version"],
            "inactivity_years": data["analysis"]["inactivity_years"],
            "release_anomaly": data["analysis"]["release_anomaly"],
            "base_score": final_risk["base_score"],
            "propagated_score": final_risk["propagated_score"],
            "final_score": final_risk["final_score"],
            "risk_category": final_risk["category"],
            "reasons": data["reasons"]   # <- RESTORED TEXTUAL REASONS
        })

    # -------------------------------------------------
    # STEP 4: Export results
    # -------------------------------------------------
    generate_risk_csv(results)


if __name__ == "__main__":
    main()