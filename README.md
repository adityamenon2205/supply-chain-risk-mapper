# 🔐 Risk Mapper for a Vector of Supply Chain Attack (open-source python packages) 

Supply Chain Risk Mapper is a Python-based security analysis tool designed to evaluate software dependency risks within a project.

It analyzes installed packages and assigns risk scores based on multiple supply chain threat indicators.

---

## 🚀 What It Does

The tool scans a project's dependencies and evaluates risk using:

- 📦 Maintainer activity analysis
- 🕒 Release inactivity detection
- 🌐 GitHub repository intelligence (stars, archive status, activity)
- 🔎 Typosquatting detection (name similarity to popular packages)
- 🔗 Dependency graph risk propagation

Each package is assigned:
- Base Risk Score
- Propagated Risk Score
- Final Risk Category (LOW / MEDIUM / HIGH)
- Human-readable risk explanations

Results are exported to a structured CSV report.

---

## 🏗️ Architecture Overview

The system follows a modular design:

- `extractor/` → Dependency extraction
- `collectors/` → PyPI & GitHub data collection
- `analyzer/` → Risk signal analysis modules
- `scoring/` → Risk scoring and propagation engine
- `output/` → CSV report generation

---

## 🔑 Setup

### 1️⃣ Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt

### 3️⃣ Configure GitHub Token

Create a `.env` file in the project root directory:

```bash
touch .env
```

Open the file and add your GitHub Personal Access Token:

```
GITHUB_TOKEN=your_github_personal_access_token
```

⚠ Make sure `.env` is added to your `.gitignore` file to prevent accidental exposure.

---

### 4️⃣ Run the Scanner

```bash
python3 main.py
```

After execution, a CSV report will be generated:

```
dependency_risk_report.csv
```
