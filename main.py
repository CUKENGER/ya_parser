from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from parser_functions import scroll_to_bottom, parse_product, safe_find_element
from set import url

output_json = 'output_json'
os.makedirs(output_json, exist_ok=True)

options = Options()
# options.add_argument('--headless')
webdriver_service = Service('./driver_win/chromedriver.exe')

def process_page(page_number):
	driver = webdriver.Chrome(service=webdriver_service, options=options)
	try:
		driver.get(url)

		for _ in range(page_number):
			try:
				next_page_btn = driver.find_element(By.XPATH, '//*[@data-auto="pagination-next"]')
				next_page_btn.click()
			except NoSuchElementException:
				print('pages not found')
				break

		scroll_to_bottom(driver)

		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, '//*[@data-index="1"]'))
		)

		products_info = []

		for i in range(1, 27):
			products_carts = driver.find_elements(By.XPATH, '//*[@data-index="{}"]'.format(i))

			for product_cart in products_carts:
				product_info = parse_product(driver, product_cart, i)
				if product_info:
					products_info.append(product_info)

			scroll_to_bottom(driver)
			time.sleep(2)

		output_path = os.path.join(output_json, f'products_info_page_{page_number}.json')
		with open(output_path, 'w', encoding='utf-8') as json_file:
			json.dump(products_info, json_file, ensure_ascii=False, indent=4)
		print(f'Информация со страницы {page_number} сохранена в {output_path}')

	except Exception as e:
		print("Ошибка:", e)

	finally:
		driver.quit()
		print(f"Парсер для страницы {page_number} завершил свою работу")

if __name__ == "__main__":
	page_numbers = range(1, 30)

	with ThreadPoolExecutor(max_workers=5) as executor:  # Установите количество воркеров в соответствии с вашими потребностями
		executor.map(process_page, page_numbers)
