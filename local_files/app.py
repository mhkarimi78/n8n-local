# local_files/app.py
from flask import Flask, request, jsonify
import sys

# اضافه کردن مسیر اسکریپت‌ها
sys.path.append("/files/scripts")

# ایمپورت دو تا ماژول
from lseg_scraper import get_esg_score
from pdf_finder import find_sustainability_pdf

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json() or {}
    company_input = data.get("company", "Apple").strip()

    # ۱. گرفتن ESG Score از LSEG
    lseg_result = get_esg_score(company_input)

    # اگر شرکت پیدا نشد
    if not lseg_result.get("found", False):
        return jsonify({
            "company": company_input,
            "found": False,
            "message": "Company not found in LSEG database"
        })

    company_name = lseg_result["company"]

    # ۲. پیدا کردن PDF گزارش پایداری
    pdf_url = find_sustainability_pdf(company_name)

    # ۳. خروجی نهایی (همه چیز با هم)
    result = {
        "company": company_name,
        "esg_score": lseg_result["esg_score"],
        "E": lseg_result.get("E", "N/A"),
        "S": lseg_result.get("S", "N/A"),
        "G": lseg_result.get("G", "N/A"),
        "year": lseg_result["year"],
        "found": True,
        "pdf_url": pdf_url or None,
        "pdf_found": bool(pdf_url)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)