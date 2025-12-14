# scripts/extract_gri.py
import google.generativeai as genai, json, sys, os

genai.configure(api_key="YOUR_GEMINI_API_KEY")

GRI_CONTEXT = ""
for file in os.listdir("../gri_docs"):
    with open(f"../gri_docs/{file}", "r", encoding="utf-8") as f:
        GRI_CONTEXT += f.read() + "\n"

def extract_gri(md_content, company):
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"""
You are a GRI ESG expert. Use the GRI standards below to extract ONLY the items present in the report.

GRI Standards:
{GRI_CONTEXT[:100000]}  # محدود به توکن

Report (Markdown):
{md_content[:30000]}

For {company}, return JSON array:
[
  {{"item_code": "2-1", "description": "Organizational details", "response": "Extracted text..."}},
  ...
]
Only include items that are explicitly mentioned.
"""
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    md_path = sys.argv[1]
    company = sys.argv[2]
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()
    json_str = extract_gri(md, company)
    # پارس و سیو CSV
    import csv, re
    try:
        items = json.loads(json_str)
    except:
        items = []
    csv_path = f"outputs/gri_{company.replace(' ', '_')}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["item_code", "description", "response"])
        for item in items:
            writer.writerow([item.get("item_code", ""), item.get("description", ""), item.get("response", "")])
    print(csv_path)