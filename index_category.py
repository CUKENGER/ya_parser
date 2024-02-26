import requests
from bs4 import BeautifulSoup
import time
import re
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from set import search, headers

url = 'https://market.yandex.ru/'

options = Options()



webdriver_service = Service('./driver/chromedriver')

driver = webdriver.Chrome(service=webdriver_service, options=options)

driver.get(url)

category_index = []

try:
	body = driver.find_element(By.XPATH, '//body')

	time.sleep(3)
	WebDriverWait(driver, 15).until(
		EC.presence_of_element_located((By.XPATH, '//*[@data-baobab-name="catalog"]'))
	)

	catalog_div = driver.find_element(By.XPATH, '//*[@data-baobab-name="catalog"]')
	catalog_btn = catalog_div.find_element(By.TAG_NAME, 'button')
	catalog_btn.click()

	time.sleep(2)

	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.XPATH, '//span[@class="_3krX4"]'))
	)

	catalog_items = driver.find_elements(By.XPATH, '//span[@class="_3krX4"]')

	# time.sleep(2)

	for i in range(len(catalog_items)):

		category_name = catalog_items[i].text

		category_info = {
			'index': i,
			"category_name": category_name
		}

		category_index.append(category_info)

	with open('category_index.json', 'w', encoding='utf-8') as json_file:
		json.dump(category_index, json_file, ensure_ascii=False, indent=4)
	print('Информация сохранена в category_index.json')

except Exception as e:
	print("Ошибка в парсере индексов категорий:", e)

finally:
	driver.quit()
	print("Парсер индексов категорий завершил свою работу")
