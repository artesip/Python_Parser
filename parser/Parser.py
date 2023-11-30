import os
import re
from time import sleep
from Adapter import Adapter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear_string(s: str) -> str:
    elems = ['\n', '\t']
    for elem in elems:
        temp = s.split(elem)
        s = ''
        s = ''.join(temp)
        s = re.sub(" +", " ", s)

    temp = ""
    if s[:4] == "Дск ":
        s = s[4:]
    elif s[:5] == "Бренд":
        s = s[5:]
    elif s[:6] == "Страна":
        s = s[19:]
    elif s[:3] == "Вес":
        s = s[3:]
    elif s[:4] == "Срок":
        s = s[13:]

    return s

def parse():
    all_quotes = []
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    driver.get('https://5ka.ru/special_offers')
    driver.implicitly_wait(60)
    
    button_yes = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "btn-main.focus-btn.location-confirm__button.red")))
    driver.execute_script('arguments[0].click();', button_yes)

    try:
        while True:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "add-more-btn")))
            button_load_more = driver.find_element(By.CLASS_NAME, "add-more-btn")
            driver.execute_script('arguments[0].click();', button_load_more)
    except:
        print("I loaded all")
    sleep(3)
    product_card_buttons = driver.find_elements(By.CLASS_NAME, "product-card.item")
    for elem in product_card_buttons:
        driver.execute_script('arguments[0].click();', elem)

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "item-name-cont"))
            )
            sleep(0.3)
        except:
            print("All elements found")

        quote_name = driver.find_element(By.CLASS_NAME, "item-name-cont").text

        quote_prices = driver.find_element(By.CLASS_NAME, "item-prices")
        quote_price_now = quote_prices.find_element(By.CLASS_NAME, "price-regular").text
        quote_price_old = quote_prices.find_element(By.CLASS_NAME, "price-discount-val").text

        quote_characteristic = driver.find_elements(By.CLASS_NAME, "item-characteristic")

        temp = quote_price_now[-2:]
        quote_price_now = quote_price_now[:-2] + "." + temp
        temp = quote_price_old[-2:]
        quote_price_old = quote_price_old[:-2] + "." + temp

        q_brand, q_made_in, q_exp_d, q_weight = quote_characteristic
        quote_name = clear_string(quote_name)
        quote_price_now = clear_string(quote_price_now)
        quote_price_old = clear_string(quote_price_old)
        q_brand = clear_string(q_brand.text)
        q_made_in = clear_string(q_made_in.text)
        q_exp_d = clear_string(q_exp_d.text)
        q_weight = clear_string(q_weight.text)
        if (quote_prices != '' and quote_price_now != '' and quote_price_old != '' and q_brand != '' and q_made_in != ''
                and q_exp_d != '' and q_weight != '' and quote_name != ''):
            all_quotes.append((Adapter(
                quote_name,
                quote_price_now[3:],
                quote_price_old,
                q_brand,
                q_made_in,
                q_exp_d,
                q_weight
            )))
    driver.close()
    return all_quotes
