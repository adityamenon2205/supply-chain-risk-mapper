import csv


def generate_risk_csv(results, output_file="dependency_risk_report.csv"):

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Updated Header
        writer.writerow([
            "Package",
            "Installed Version",
            "Inactivity (Years)",
            "Release Anomaly",
            "Risk Score",
            "Risk Category",
            "Reasons"
        ])

        for result in results:
            writer.writerow([
                result["package"],
                result["version"],
                result["inactivity_years"],
                result["release_anomaly"],
                result["risk_score"],
                result["risk_category"],
                "; ".join(result["reasons"])
            ])

    print(f"\nRisk CSV generated: {output_file}")