from time import sleep
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Adapter:
    def __init__(self, name: str, price_now: str, price_old: str, brand: str, made_in: str, expiration_date: str,
                 weight: str):
        self.name = name
        self.price_now = price_now
        self.price_old = price_old
        self.brand = brand
        self.made_in = made_in
        self.expiration_date = expiration_date
        self.weight = weight


def clear_string(s: str) -> str:
    elems = ['\n', '\t']
    for elem in elems:
        temp = s.split(elem)
        s = ''
        s = ''.join(temp)
        s = re.sub(" +", " ", s)
    if s[:5] == " Дск ":
        s = s[4:]

    return s


def parse() -> list:
    all_quotes = []

    driver = webdriver.Chrome()
    driver.get('https://5ka.ru/special_offers')
    driver.implicitly_wait(10)

    button_yes = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "btn-main.focus-btn.location-confirm__button.red")))
    driver.execute_script('arguments[0].click();', button_yes)

    button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "product-card.item")))

    button = driver.find_elements(By.CLASS_NAME, "product-card.item")

    for elem in button:
        driver.execute_script('arguments[0].click();', elem)
        sleep(0.3)
        html = driver.execute_script("return document.body.innerHTML")

        bsObj = BeautifulSoup(html, 'html.parser')
        found_quote = bsObj.find('div', {'class': 'sidebar-main'})

        quote_name = found_quote.find('div', {'class': 'item-name-cont'}).text
        quote_price_now = found_quote.find('div', {'class': 'price-regular'}).text
        quote_price_old = found_quote.find('span', {'class': 'price-discount-val'}).text
        quote_characteristic = found_quote.find_all('li', {'class', 'item-characteristic'})

        q_brand, q_made_in, q_exp_d, q_weight = quote_characteristic

        quote_name = clear_string(quote_name)[1:-1]
        quote_price_now = clear_string(quote_price_now)[3:]
        quote_price_old = clear_string(quote_price_old)
        q_brand = clear_string(q_brand.text)[1:-1]
        q_made_in = clear_string(q_made_in.text)[1:-1]
        q_exp_d = clear_string(q_exp_d.text)[1:-1]
        q_weight = clear_string(q_weight.text)[1:-1]

        quote_price_now = quote_price_now[:-2] + "." + quote_price_now[-2:]
        quote_price_old = quote_price_old[:-2] + "." + quote_price_old[-2:]

        all_quotes.append(Adapter(
            quote_name,
            quote_price_old,
            quote_price_now,
            q_brand,
            q_made_in,
            q_exp_d,
            q_weight
        ))

    driver.close()

    return all_quotes
