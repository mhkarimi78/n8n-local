# local_files/scripts/lseg_scraper.py
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging
import re

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def get_esg_score(user_input):
    logging.info(f"[START] جستجو برای: {user_input}")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    service = Service('/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://www.lseg.com/en/data-analytics/sustainable-finance/esg-scores")
        time.sleep(7)

        # بستن کوکی بنر
        try:
            accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_btn.click()
            time.sleep(2)
        except:
            pass

        # جستجو
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchInput-1")))
        search_box.clear()
        search_box.send_keys(user_input)
        time.sleep(5)

        # انتخاب هوشمند بهترین شرکت
        suggestions = driver.find_elements(By.XPATH, "//li[@role='option']//button")
        if not suggestions:
            return {"company": user_input, "found": False, "error": "No suggestions"}

        clean_input = re.sub(r'\b(inc|corp|ltd|sa|as|plc|ag|nv|gmbh|co)\b\.?', '', user_input, flags=re.I).strip()
        best_match = None
        best_score = -1

        for btn in suggestions:
            full_text = btn.text.strip()
            clean_text = re.sub(r'\b(inc|corp|ltd|sa|as|plc|ag|nv|gmbh|co)\b\.?', '', full_text, flags=re.I).strip()
            score = 0
            if clean_text.lower().startswith(clean_input.lower()):
                score += 100
            elif clean_input.lower() in clean_text.lower():
                score += 50
            if any(word in full_text.lower() for word in ['inc','corp','ltd','sa','a/s','ag','plc']):
                score += 10
            if score > best_score:
                best_score = score
                best_match = (btn, full_text)

        if not best_match:
            return {"company": user_input, "found": False, "error": "No good match"}

        selected_button, selected_company_name = best_match
        selected_button.click()
        logging.info(f"[OK] انتخاب شد: {selected_company_name}")

        # صبر طولانی برای لود کامل
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3.Typestack--h3")))
        time.sleep(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # اسم دقیق شرکت و ESG اصلی
        h3 = soup.find('h3', class_='Typestack--h3')
        company_from_page = h3.get_text(strip=True).split("ESG score")[0].strip() if h3 else selected_company_name
        esg_score = h3.find('strong').get_text(strip=True) if h3 and h3.find('strong') else "N/A"
        year_tag = h3.find_next('p', class_='fiscal-year') if h3 else None
        year = year_tag.get_text(strip=True).split()[-2] if year_tag else "N/A"

        # E/S/G دقیق از بخش اصلی (نه جدول قدیمی!)
        scores = {'E': 'N/A', 'S': 'N/A', 'G': 'N/A'}
        for label, key in [("Environment", "E"), ("Social", "S"), ("Governance", "G")]:
            strong_tag = soup.find('strong', string=re.compile(label, re.I))
            if strong_tag:
                # عدد بزرگ بعدی (درون b یا div)
                next_b = strong_tag.find_next('b')
                if next_b and next_b.get_text(strip=True).isdigit():
                    scores[key] = next_b.get_text(strip=True)
                else:
                    # اگر b نبود، از div بعدی که فقط عدد داره
                    next_div = strong_tag.find_next(string=re.compile(r'^\s*\d+\s*$'))
                    if next_div:
                        scores[key] = re.search(r'\d+', next_div).group()

        logging.info(f"[SUCCESS] {company_from_page} → ESG: {esg_score} | E:{scores['E']} S:{scores['S']} G:{scores['G']} | Year: {year}")

        return {
            "company": company_from_page,
            "esg_score": esg_score,
            "E": scores['E'],
            "S": scores['S'],
            "G": scores['G'],
            "year": year,
            "found": True
        }

    except Exception as e:
        logging.error(f"[ERROR] {user_input}: {e}")
        return {"company": user_input, "found": False, "error": str(e)}
    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company = sys.argv[1]
    else:
        company = "Apple"  # اگر چیزی ندادی، پیش‌فرض Apple تست می‌کنه
    result = get_esg_score(company)
    print(json.dumps(result, ensure_ascii=False, indent=2))