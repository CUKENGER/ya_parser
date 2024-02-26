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

actions = ActionChains(driver)

number_category = 5

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
	
	actions.move_to_element(catalog_items[number_category]).perform()

	time.sleep(2)

	subcat_btns = driver.find_elements(By.XPATH, '//span[@class="_1xQHu"]')

	for btn in subcat_btns:
		btn.click()

	subcat_div = driver.find_elements(By.XPATH, '//*[@data-baobab-name="linkSnippet"]')

	for subcat in subcat_div:

		subcat_cont = subcat.find_element(By.TAG_NAME, 'a')
		name = subcat_cont.text
		print(f'name: {name}')
		link_subcat = subcat_cont.get_attribute('href')
		print(f'link: {link_subcat}')

except Exception as e:
	print("Ошибка:", e)

finally:
	driver.quit()
	print("Парсер завершил свою работу")
