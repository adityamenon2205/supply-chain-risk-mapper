from extractor.dependency_extractor import DependencyExtractor
from collectors.pypi_collector import PyPICollector
from collectors.github_collector import GitHubCollector
from analyzer.maintainer_analysis import MaintainerAnalyzer
from analyzer.github_analysis import GitHubAnalyzer
from scoring.risk_engine import RiskEngine
from output.json_to_csv import generate_risk_csv


def main():
    extractor = DependencyExtractor(".")
    dependencies = extractor.extract()

    collector = PyPICollector()
    github_collector = GitHubCollector()
    analyzer = MaintainerAnalyzer()
    github_analyzer = GitHubAnalyzer()
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
    # STEP 2: Compute base risks (including GitHub signals)
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

        # -------------------------------
        # GitHub Integration
        # -------------------------------
        github_url = None

        project_urls = metadata.get("project_urls", {})

        if isinstance(project_urls, dict):
            github_url = (
                project_urls.get("Source")
                or project_urls.get("Homepage")
                or project_urls.get("Repository")
            )

        if not github_url:
            github_url = metadata.get("home_page")

        github_data = None
        if github_url and "github.com" in github_url:
            github_data = github_collector.fetch_repo_data(github_url)

        github_analysis = github_analyzer.analyze(github_data)

        # -------------------------------
        # Combine Maintainer + GitHub score
        # -------------------------------
        combined_maintainer_score = (
            analysis["maintainer_score"] + github_analysis["github_score"]
        )

        base_data = risk_engine.calculate_base_risk(
            package_name=package_name,
            maintainer_score=combined_maintainer_score,
            inactivity_years=analysis["inactivity_years"],
            dependency_count=dependency_count
        )

        # Merge textual reasons
        combined_reasons = (
            base_data["reasons"] + github_analysis["github_reasons"]
        )

        package_analysis_cache[package_name] = {
            "version": version,
            "analysis": analysis,
            "dependency_count": dependency_count,
            "reasons": combined_reasons
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
            "reasons": data["reasons"]
        })

    # -------------------------------------------------
    # STEP 4: Export results
    # -------------------------------------------------
    generate_risk_csv(results)


if __name__ == "__main__":
    main()