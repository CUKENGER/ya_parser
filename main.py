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

search = 'iphone'

url = f"https://market.yandex.ru/catalog--mobilnye-telefony/34512430/list?was_redir=1&rt=11&rs=eJx9kc0vA1EUxd-raiaPxVuJVsSLj6QSEm2xoTJYS_wF3oxJk47IdNJpLQSZFQk2KGEhakUQRCKRKLpB2FjZWdTH0sZCRFiYe1nb_HLnzrnnnjsTvSur72AB006mrAS_enosq_crhAeQ5JdhMkLGA5GOWFt7zKXPt-Wz1KeQQTruV7yHHcqUlYeHSr7_vlpxSMklJa4V91jcA5ZmClDnzjyq08DSB_TJFNZb8JZ8A0tNPaCc7vYomqHjtuDUe5dHbRun4nH0QX-keoAO16DUhlDfCH13E2pyBLV2j0mWkGnk7ik4TMGuorzwmF_HjRyTBEEjWtEtirtuIENxErPN4957rE9Q2Yk-y8D8IjhoQazHUBPCJEG4Tnyiv4vfpBf6YgOS5OfwOoZX9JyDfx30tX7Yq-ZQXwAKFae-oFYb8JYqYH7hN8lZ3xplrUxRKC-vpoJyX6jGsHXpJFO2NC0jm5Fp00hKxzJtO5ER3t9lEZQr1X7h5zxUM6w7piENPZ3KOolRaY_qpiWdhJ42kuJ1QYbfCgMs9jfCBPNGav8ZkVGRW5kIH78McPoDWjLNfA%2C%2C&parsed-glfilter=7893318%3A153043&text={search}&hid=91491&local-offers-first=0&glfilter=7893318%3A153043"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

options = Options()

webdriver_service = Service('./driver/chromedriver')

driver = webdriver.Chrome(service=webdriver_service, options=options)

driver.get(url)

try:
    body = driver.find_element(By.XPATH, '//body')
    body.send_keys(Keys.END)
    time.sleep(3)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@data-index="1"]'))
    )

    products_info = []

    for i in range(1, 15):
        products_carts = driver.find_elements(By.CLASS_NAME, 'nXZ_7')
        print(f"products_carts:{i}{products_carts}")

        for product_cart in products_carts:
            try:
                index = len(products_carts) + i
                # raw_price = product_cart.find_element(By.CLASS_NAME, '_8-sD9').text
                # price = re.sub(r'^[0-9₽]', '', raw_price)
                # print(f'price:{price}')
                # link_element = product_cart.find_element(By.CLASS_NAME, '_2Fl2z')
                link_div = product_cart.find_element(By.XPATH, '//*[@data-baobab-name="title"]').text
                # link_element = product_cart.find_element(By.XPATH, '//*[@aria-hidden="false"]')
                link_element = link_div.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')
                print(f'link:{link}')
                # name = product_cart.find_element(By.CLASS_NAME, '_1zh3_').text
                # print(f'name{name}')

                product_info = {
                    'index': index,
                    # 'name': name,
                    # 'price': price,
                    'link': link
                }
                products_info.append(product_info)

            except Exception as ex:
                print(f"Error processing product: {ex}")

        body = driver.find_element(By.XPATH, '//body')
        body.send_keys(Keys.END)
        time.sleep(2)

    with open('products_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(products_info, json_file, ensure_ascii=False, indent=4)
    print('Информация сохранена в products_info.json')

except Exception as e:
    print("Ошибка:", e)

finally:
    driver.quit()
    print("Парсер завершил свою работу")
