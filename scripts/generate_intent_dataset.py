"""
Generate Intent Classification Dataset using Gemini

Input:
    data/raw/RAG_DB_CANONICAL_Marathi.json

Output:
    data/datasets/intent/intent_dataset.csv
"""

import os
import json
import csv
import time

import google.generativeai as genai

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

#model = genai.GenerativeModel("gemini-2.5-pro")
# Or use:
model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

INPUT_FILE =r"D:\SLM Finetuning\DBTCitizenBot-SLM-Finetuning\data\raw\RAG_DB_CANONICAL_Marathi.json"
OUTPUT_FILE = r"D:\SLM Finetuning\DBTCitizenBot-SLM-Finetuning\data\datasets\intent\intent_dataset.csv"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# ----------------------------------------------------------
# Prompt
# ----------------------------------------------------------

SYSTEM_PROMPT = """
You are preparing a supervised fine-tuning dataset for the DBT Citizen Bot.

Classify the user question.

Allowed intents:

- SCHEME_INFO
- SCHEME_FIELD_QUERY
- ELIGIBILITY_MATCH
- FILTER_SEARCH
- DOCUMENT_QUERY
- BENEFIT_QUERY
- APPLICATION_PROCESS
- APPLICATION_STATUS
- REJECTION_HELP
- COMPARISON
- FOLLOW_UP
- DEPARTMENT_QUERY

Allowed field_focus:

- eligibility
- documents
- benefit
- how_to_apply
- income_limit
- dept
- deadline

Allowed query_focus:

- list_expand

Rules:

Return ONLY valid JSON.

Example:

{
    "intent":"FILTER_SEARCH",
    "field_focus":null,
    "query_focus":"list_expand"
}
"""

# ----------------------------------------------------------
# Gemini Call
# ----------------------------------------------------------

def classify_question(question):

    prompt = f"""
Question:

{question}
"""

    for attempt in range(3):

        try:

            response = model.generate_content(
                [
                    SYSTEM_PROMPT,
                    prompt
                ],
                generation_config=genai.GenerationConfig(
                    temperature=0,
                    response_mime_type="application/json"
                )
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            return json.loads(text)

        except Exception as e:

            print(f"Retry {attempt+1}: {e}")

            time.sleep(2)

    return {
        "intent": "",
        "field_focus": "",
        "query_focus": ""
    }

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

# ----------------------------------------------------------
# Process Questions
# ----------------------------------------------------------

for idx, item in enumerate(data, start=1):

    print(f"Processing {idx}/{len(data)}")

    english = item.get("question", "").strip()

    if english:

        result = classify_question(english)

        rows.append({
            "question": english,
            "language": "en",
            "intent": result.get("intent"),
            "field_focus": result.get("field_focus"),
            "query_focus": result.get("query_focus"),
            "source": "canonical"
        })

    marathi = item.get("marathi_question", "").strip()

    if marathi:

        result = classify_question(marathi)

        rows.append({
            "question": marathi,
            "language": "mr",
            "intent": result.get("intent"),
            "field_focus": result.get("field_focus"),
            "query_focus": result.get("query_focus"),
            "source": "canonical"
        })

    time.sleep(0.5)

# ----------------------------------------------------------
# Save CSV
# ----------------------------------------------------------

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "question",
            "language",
            "intent",
            "field_focus",
            "query_focus",
            "source"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print("\nDone!")
print(f"Generated {len(rows)} rows")
print(f"Saved to: {OUTPUT_FILE}")
