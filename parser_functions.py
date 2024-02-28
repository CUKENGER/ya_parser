
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

def scroll_to_bottom(driver):
	body = driver.find_element(By.XPATH, '//body')
	body.send_keys(Keys.END)
	time.sleep(3)
	wait = WebDriverWait(driver, 10)

def parse_product(driver, product_cart, i):
	try:
		index = i

		wait = WebDriverWait(driver, 10)

		try:

			raw_price_div = wait.until(EC.presence_of_element_located((By.XPATH, './/span[@data-auto="snippet-price-old"]')))

			raw_price_div = product_cart.find_element(By.XPATH, './/span[@data-auto="snippet-price-old"]')

			if raw_price_div:
				# raw_price_element = raw_price_div.find_element(By.XPATH, '//span[@class="_1oI3I"]')
				raw_price = raw_price_div.text
				print('raw_price-el:')

		except NoSuchElementException:
			print('raw_price_div not found. Search other')
			try:

				raw_price_element = raw_price_div.find_element(By.XPATH, '//span[@data-auto="price-value"]')
				raw_price = raw_price_element.text


			except NoSuchElementException:
				print('No one element found')

		price = re.sub(r'[^\d₽]', '', raw_price)

		try:

			name = product_cart.find_element(By.XPATH, './/h3[@data-auto="snippet-title-header"]/a/span').text
		except NoSuchElementException:
			name = 'hui'

		try:

			link_element = product_cart.find_element(By.XPATH, './/h3[@data-auto="snippet-title-header"]/a')
			link = link_element.get_attribute('href')
		except NoSuchElementException:
			link = 'https://poshel na hui'

		product_info = {
			'index': index,
			'name': name,
			'price': price,
			'link': link
		}
		return product_info

	except Exception as ex:
		print(f"Error processing product: {ex}")
		return None
