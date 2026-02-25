class RiskEngine:
    def __init__(self):
        # Store base risk before propagation
        self.base_risk = {}      # {package: base_score}
        self.final_risk = {}     # {package: final_score}
        self.graph = {}          # {package: [dependencies]}

    # -----------------------------------------------------
    # Step 1: Add package and its dependencies to graph
    # -----------------------------------------------------
    def add_package(self, package_name, dependencies):
        if package_name not in self.graph:
            self.graph[package_name] = dependencies or []

    # -----------------------------------------------------
    # Step 2: Calculate base risk (original logic improved)
    # -----------------------------------------------------
    def calculate_base_risk(self, package_name, maintainer_score, inactivity_years, dependency_count):
        score = 0
        reasons = []

        # Maintainer risk
        if maintainer_score >= 2:
            score += 3
            reasons.append("Maintainer instability detected.")

        # Inactivity risk
        if inactivity_years >= 2:
            score += 3
            reasons.append("Project inactive for over 2 years.")

        # Large dependency surface
        if dependency_count >= 5:
            score += 2
            reasons.append("Large dependency surface increases attack exposure.")

        # Store base risk
        self.base_risk[package_name] = score

        return {
            "base_score": score,
            "reasons": reasons
        }

    # -----------------------------------------------------
    # Step 3: Risk Propagation (Recursive with Dampening)
    # -----------------------------------------------------
    def _propagate_risk(self, package_name, visited=None, depth=0):
        if visited is None:
            visited = set()

        if package_name in visited:
            return 0  # Prevent infinite loops (cycles)

        visited.add(package_name)

        total_propagated = 0
        dependencies = self.graph.get(package_name, [])

        for dep in dependencies:
            dep_base = self.base_risk.get(dep, 0)

            # Dampening factor (deeper dependencies contribute less)
            propagation_factor = 0.3
            depth_factor = 1 / (depth + 1)

            propagated_value = dep_base * propagation_factor * depth_factor
            total_propagated += propagated_value

            # Recursive call for transitive dependencies
            total_propagated += self._propagate_risk(dep, visited, depth + 1)

        return total_propagated

    # -----------------------------------------------------
    # Step 4: Compute Final Risk with Propagation
    # -----------------------------------------------------
    def calculate_final_risk(self, package_name):
        base = self.base_risk.get(package_name, 0)
        propagated = self._propagate_risk(package_name)

        final_score = base + propagated
        self.final_risk[package_name] = final_score

        # Classification
        if final_score >= 8:
            category = "HIGH"
        elif final_score >= 4:
            category = "MEDIUM"
        else:
            category = "LOW"

        return {
            "base_score": base,
            "propagated_score": round(propagated, 2),
            "final_score": round(final_score, 2),
            "category": category
        }

    # -----------------------------------------------------
    # Step 5: Run Full Risk Evaluation
    # -----------------------------------------------------
    def evaluate_package(self, package_name, maintainer_score, inactivity_years, dependency_count, dependencies):
        # Add package to graph
        self.add_package(package_name, dependencies)

        # Calculate base risk
        base_data = self.calculate_base_risk(
            package_name,
            maintainer_score,
            inactivity_years,
            dependency_count
        )

        # Calculate final risk
        final_data = self.calculate_final_risk(package_name)

        return {
            "package": package_name,
            "base_score": final_data["base_score"],
            "propagated_score": final_data["propagated_score"],
            "final_score": final_data["final_score"],
            "category": final_data["category"],
            "reasons": base_data["reasons"]
        }