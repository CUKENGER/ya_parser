
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def scroll_to_bottom(driver):
    body = driver.find_element(By.XPATH, '//body')
    body.send_keys(Keys.END)
    time.sleep(3)

def parse_product(product_cart, i):
    try:
        index = i
        raw_price_div = product_cart.find_element(By.XPATH, './/div[@data-baobab-name="price"]')

        if raw_price_div:
        	raw_price_element = raw_price_div.find_element(By.XPATH, '//h3[@class="_1He5n _36SPc _2kgEE _1KE2k _1cQ6F d459O"]')
        	if raw_price_element:
        		raw_price = raw_price_element.text
        	else:
        		raw_price_element = raw_price_div.find_element(By.XPATH, '//span[@class="_8-sD9"]')
        		raw_price = raw_price_element.text
	        
        price = re.sub(r'[^\d₽]', '', raw_price)

        name = product_cart.find_element(By.XPATH, './/h3[@data-auto="snippet-title-header"]/a/span').text

        link_element = product_cart.find_element(By.XPATH, './/h3[@data-auto="snippet-title-header"]/a')
        link = link_element.get_attribute('href')

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
