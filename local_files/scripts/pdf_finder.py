import subprocess
import json

def find_sustainability_pdf(company_name, year=None):
    year = year or 2024

    # اجرای فایل JS با node
    try:
        cmd = ["node", "/files/scripts/esgreport_scraper/scraper.mjs", company_name, str(year)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            logging.error(f"JS error: {result.stderr}")
            return "NotFound"

        # خروجی JS رو parse کن (فرض می‌کنیم JS فقط لینک رو print می‌کنه)
        output = result.stdout.strip()
        if output.startswith("http") and output.endswith(".pdf"):
            return output
        else:
            return "NotFound"

    except Exception as e:
        logging.error(f"Error running JS: {e}")
        return "NotFound"