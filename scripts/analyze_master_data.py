import json
import os
from collections import Counter
import pandas as pd

# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT_FILE = r"D:\SLM Finetuning\DBTCitizenBot-SLM-Finetuning\data\raw\official_master.json"
OUTPUT_DIR = r"data\analysis"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Load JSON
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    schemes = json.load(f)

print(f"Loaded {len(schemes)} schemes.")

# --------------------------------------------------
# Counters
# --------------------------------------------------

departments = Counter()
short_names = Counter()
groups = Counter()

castes = Counter()
levels = Counter()
beneficiaries = Counter()
benefits = Counter()
income_tags = Counter()

missing = Counter()

eligibility_sentences = Counter()
rule_sentences = Counter()

scheme_stats = []

# --------------------------------------------------
# Iterate Schemes
# --------------------------------------------------

for scheme in schemes:

    name = scheme.get("name", "")

    # ------------------------
    # Department
    # ------------------------

    dept = scheme.get("dept")

    if dept:
        departments[dept] += 1
    else:
        missing["dept"] += 1

    # ------------------------

    short = scheme.get("short")

    if short:
        short_names[short] += 1
    else:
        missing["short"] += 1

    # ------------------------

    group = scheme.get("group")

    if group:
        groups[group] += 1
    else:
        missing["group"] += 1

    # ------------------------
    # Eligibility
    # ------------------------

    elig = scheme.get("elig", [])

    if len(elig) == 0:
        missing["elig"] += 1

    for sentence in elig:
        eligibility_sentences[sentence] += 1

    # ------------------------
    # Rules
    # ------------------------

    rules = scheme.get("rule", [])

    if len(rules) == 0:
        missing["rule"] += 1

    for sentence in rules:
        rule_sentences[sentence] += 1

    # ------------------------
    # Benefits
    # ------------------------

    ben = scheme.get("benefits", [])

    if len(ben) == 0:
        missing["benefits"] += 1

    # ------------------------
    # Documents
    # ------------------------

    docs = scheme.get("docs", [])

    if len(docs) == 0:
        missing["docs"] += 1

    # ------------------------
    # Tags
    # ------------------------

    tags = scheme.get("tags", {})

    for c in tags.get("caste", []):
        castes[c] += 1

    for l in tags.get("level", []):
        levels[l] += 1

    for b in tags.get("beneficiary", []):
        beneficiaries[b] += 1

    for b in tags.get("benefit", []):
        benefits[b] += 1

    for i in tags.get("income", []):
        income_tags[i] += 1

    # ------------------------
    # Statistics
    # ------------------------

    scheme_stats.append({

        "Scheme Name": name,

        "Department": dept,

        "Eligibility Count": len(elig),

        "Rule Count": len(rules),

        "Benefit Count": len(ben),

        "Document Count": len(docs),

        "Caste Tags": len(tags.get("caste", [])),

        "Beneficiary Tags": len(tags.get("beneficiary", [])),

        "Level Tags": len(tags.get("level", []))
    })

# --------------------------------------------------
# Helper
# --------------------------------------------------

def save_counter(counter, filename, column):

    df = pd.DataFrame(counter.items(), columns=[column, "Count"])

    df = df.sort_values("Count", ascending=False)

    df.to_csv(
        os.path.join(OUTPUT_DIR, filename),
        index=False
    )

# --------------------------------------------------
# Save CSVs
# --------------------------------------------------

save_counter(departments, "departments.csv", "Department")
save_counter(short_names, "short_names.csv", "Short")
save_counter(groups, "groups.csv", "Group")

save_counter(castes, "castes.csv", "Caste")
save_counter(levels, "levels.csv", "Level")
save_counter(beneficiaries, "beneficiaries.csv", "Beneficiary")
save_counter(benefits, "benefit_tags.csv", "Benefit")
save_counter(income_tags, "income_tags.csv", "Income")

save_counter(eligibility_sentences,
             "eligibility_rules.csv",
             "Eligibility Rule")

save_counter(rule_sentences,
             "scheme_rules.csv",
             "Scheme Rule")

pd.DataFrame(scheme_stats).to_csv(
    os.path.join(OUTPUT_DIR,
                 "scheme_statistics.csv"),
    index=False
)

pd.DataFrame(
    missing.items(),
    columns=["Field", "Missing Count"]
).to_csv(
    os.path.join(OUTPUT_DIR,
                 "missing_fields.csv"),
    index=False
)

# --------------------------------------------------
# Markdown Report
# --------------------------------------------------

report = f"""
# DBT Master Data Analysis

## Overall Statistics

|Metric|Count|
|------|----:|
|Total Schemes|{len(schemes)}|
|Departments|{len(departments)}|
|Groups|{len(groups)}|
|Short Names|{len(short_names)}|

## Tag Statistics

|Tag|Unique Values|
|---|---:|
|Caste|{len(castes)}|
|Beneficiary|{len(beneficiaries)}|
|Level|{len(levels)}|
|Benefit|{len(benefits)}|
|Income|{len(income_tags)}|

## Missing Fields

"""

for field, count in missing.items():
    report += f"- {field}: {count}\n"

with open(
        os.path.join(OUTPUT_DIR,
                     "analysis_report.md"),
        "w",
        encoding="utf-8") as f:

    f.write(report)

print("\nAnalysis Complete")
print(f"Files saved to {OUTPUT_DIR}")