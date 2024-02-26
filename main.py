import requests
from bs4 import BeautifulSoup
import time
import re
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from parser_functions import scroll_to_bottom, parse_product
from set import url, search, headers

output_json= 'output_json'
os.makedirs(output_json, exist_ok=True)
options = Options()

webdriver_service = Service('./driver/chromedriver')

driver = webdriver.Chrome(service=webdriver_service, options=options)

driver.get(url)

try:
    scroll_to_bottom(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@data-index="1"]'))
    )

    products_info = []

    for i in range(1, 25):
        products_carts = driver.find_elements(By.XPATH, '//*[@data-index="{}"]'.format(i))

        for product_cart in products_carts:
        	product_info = parse_product(product_cart, i)
        	if product_info:
        		products_info.append(product_info)

        scroll_to_bottom(driver)
        time.sleep(2)

    output_path = os.path.join(output_json, 'products_info.json')
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(products_info, json_file, ensure_ascii=False, indent=4)
    print(f'Информация сохранена в {output_path}')

except Exception as e:
    print("Ошибка:", e)

finally:
    driver.quit()
    print("Парсер завершил свою работу")
