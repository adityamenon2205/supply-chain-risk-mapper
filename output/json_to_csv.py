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
            "Base Risk Score",
            "Propagated Risk Score",
            "Final Risk Score",
            "Risk Category",
            "Reasons"
        ])

        for result in results:

            # Show textual reasons only for MEDIUM and HIGH risks
            if result["risk_category"] in ["MEDIUM", "HIGH"]:
                reasons_text = "; ".join(result.get("reasons", []))
            else:
                reasons_text = ""

            writer.writerow([
                result["package"],
                result["version"],
                result["inactivity_years"],
                result["release_anomaly"],
                result["base_score"],
                result["propagated_score"],
                result["final_score"],
                result["risk_category"],
                reasons_text
            ])

    print(f"\nRisk CSV generated: {output_file}")