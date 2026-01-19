import sys, os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait, Select
from urllib.request import urlretrieve
from sql import cty_pop_sql
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def update_city_pop() :
    path = 'chromedriver.exe'
    service = webdriver.chrome.service.Service(path)
    driver = webdriver.Chrome(service=service)

    url = "https://jumin.mois.go.kr/"
    driver.get(url)

    wait = WebDriverWait(driver, 15)

    iframe = driver.find_element(By.TAG_NAME, "iframe")

    driver.switch_to.default_content()
    driver.switch_to.frame(iframe)

    driver.find_elements(By.NAME, 'searchYearMonth')[1].click()
    time.sleep(1)
    searchYearStart = Select(driver.find_element(By.ID, "searchYearStart"))
    searchYearStart.select_by_value('2020')
    searchYearEnd = Select(driver.find_element(By.ID, "searchYearEnd"))
    searchYearEnd.select_by_value('2024')

    driver.find_element(By.ID, 'sex1').click()
    driver.find_element(By.ID, 'sex2').click()
    driver.find_element(By.CLASS_NAME, 'btn_search').click()

    time.sleep(2)

    tr_list = driver.find_element(By.ID, 'contextTable').find_elements(By.CSS_SELECTOR, 'tbody tr')

    city_population_list = []
    years = [2020, 2021, 2022, 2023, 2024]

    for tr in tr_list:
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) < 15:
            continue

        city = tds[1].text.strip()
        if not city:
            continue

        for k, year in enumerate(years):
            idx = 2 + (k * 3)
            pop_text = tds[idx].text.strip().replace(",", "")
            if not pop_text:
                continue
            city_population_list.append((city.replace('* ', ''), year, int(pop_text)))
    driver.quit()

    result = cty_pop_sql.insert_cty_pop(city_population_list)
    print(result,'성공')

def select_city_pop() :
    rows = cty_pop_sql.select_cty_pop({'CTY_CODE': 11})
    for r in rows:
        print(r)

update_city_pop()
# select_city_pop()