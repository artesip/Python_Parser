from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Adapter import Adapter


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
        temp = s[5:]
        s = s[:5] + ' ' + temp
    elif s[:6] == "Страна":
        temp = s[19:]
        s = s[:19] + ' ' + temp
    elif s[:3] == "Вес":
        temp = s[3:]
        s = s[:3] + ' ' + temp
    elif s[:4] == "Срок":
        temp = s[13:]
        s = s[:13] + ' ' + temp

    return s


def parse() -> list:
    all_quotes = []

    driver = webdriver.Chrome()
    driver.get('https://5ka.ru/special_offers')
    driver.implicitly_wait(10)

    button_yes = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "btn-main.focus-btn.location-confirm__button.red")))
    driver.execute_script('arguments[0].click();', button_yes)

    try:
        while True:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "add-more-btn")))
            button_load_more = driver.find_element(By.CLASS_NAME, "add-more-btn")
            driver.execute_script('arguments[0].click();', button_load_more)
    except:
        print("I loaded all")

    product_card_buttons = driver.find_elements(By.CLASS_NAME, "product-card.item")

    for elem in product_card_buttons:
        driver.execute_script('arguments[0].click();', elem)

        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "item-name-cont"))
            )
            sleep(0.1)
        except:
            print("All elements found")

        quote_name_2 = driver.find_element(By.CLASS_NAME, "item-name-cont").text

        quote_prices = driver.find_element(By.CLASS_NAME, "item-prices")
        quote_price_now_2 = quote_prices.find_element(By.CLASS_NAME, "price-regular").text
        quote_price_old_2 = quote_prices.find_element(By.CLASS_NAME, "price-discount-val").text

        quote_characteristic_2 = driver.find_elements(By.CLASS_NAME, "item-characteristic")

        temp = quote_price_now_2[-2:]
        quote_price_now_2 = quote_price_now_2[:-2] + "." + temp
        temp = quote_price_old_2[-2:]
        quote_price_old_2 = quote_price_old_2[:-2] + "." + temp

        q_brand_2, q_made_in_2, q_exp_d_2, q_weight_2 = quote_characteristic_2
        quote_name_2 = clear_string(quote_name_2)
        quote_price_now_2 = clear_string(quote_price_now_2)
        quote_price_old_2 = clear_string(quote_price_old_2)
        q_brand_2 = clear_string(q_brand_2.text)
        q_made_in_2 = clear_string(q_made_in_2.text)
        q_exp_d_2 = clear_string(q_exp_d_2.text)
        q_weight_2 = clear_string(q_weight_2.text)

        all_quotes.append((Adapter(
            quote_name_2,
            quote_price_now_2[3:],
            quote_price_old_2,
            q_brand_2,
            q_made_in_2,
            q_exp_d_2,
            q_weight_2
        )))
    driver.close()
    return all_quotes
