import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlretrieve
from sql import faq_sql

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def update_faq2() :
    path = 'chromedriver.exe'
    service = webdriver.chrome.service.Service(path)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)
    
    url = "https://main.kotsa.or.kr/portal/bbs/faq_list.do?menuCode=04010100"
    driver.get(url)

    faq_list = []
    
    li_list = driver.find_elements(By.CSS_SELECTOR, 'div[data-bbslist="faq"] ul li')
    for li in li_list:
        question = li.find_element(By.TAG_NAME, 'a').get_attribute('textContent').replace("질문", "", 1).strip()
        answer = li.find_element(By.CSS_SELECTOR, 'div[data-bbsbody="conts"]').get_attribute('textContent').replace("답변", "", 1).strip()
        faq_list.append((question, answer, '한국교통안전공단'))
    driver.quit()
    success = faq_sql.insert_faq(faq_list, '한국교통안전공단')
    print(success, '성공')
update_faq2()
