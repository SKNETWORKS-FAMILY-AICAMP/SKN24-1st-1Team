import sys, os, re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sql import faq_sql

import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

base = "https://eminwon.molit.go.kr"

# 디테일 내용은 faqContents.do API에서 HTML의 내용 가져오기 때문에 따로 BEAUTIFULSOUP 사용
def get_faq_detail(session, faq_id):
    url = base + "/faqContents.do?"
    r = session.post(url, data={"faqId": str(faq_id)}, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    answer = ""
    for tr in soup.select("table.table_view tbody tr"):
        th = tr.select_one("th")
        if th and th.get_text(strip=True) == "회신내용":
            td = tr.select_one("td")
            answer = td.get_text("\n", strip=True) if td else ""
            break
    return answer

def update_faq1():
    driver_path = Path(__file__).resolve().parent / "chromedriver.exe"
    service = webdriver.chrome.service.Service(str(driver_path))
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(base + "/faqList.do?")
        wait = WebDriverWait(driver, 15)

        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchKeyword")))
        search_box.clear()
        search_box.send_keys("차량")
        search_box.send_keys(Keys.RETURN)

        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".table_list a[onclick*='fn_select_faqContents']")
        ))

        links = driver.find_elements(By.CSS_SELECTOR, ".table_list a[onclick*='fn_select_faqContents']")

        session = requests.Session()
        session.headers.update({"User-Agent": driver.execute_script("return navigator.userAgent;")})

        faq_list = []
        for a in links:
            onclick = a.get_attribute("onclick") or ""
            m = re.search(r"fn_select_faqContents\('(\d+)'\)", onclick)
            if not m:
                continue
            
            # onclick attr안에 있는 faq_id 받아오기
            faq_id = m.group(1)
            question = a.text.strip()
            if not question:
                continue
            
            # 디테일 내용은 faqContents.do API에서 HTML의 내용 가져오기 때문에 따로 BEAUTIFULSOUP 사용
            answer = get_faq_detail(session, faq_id)
            faq_list.append((question, answer, '국토교통부 민원마당'))

        result = faq_sql.insert_faq(faq_list, '국토교통부 민원마당')
        print(result,'성공')

    finally:
        driver.quit()

# 크롤링 실행
update_faq1()