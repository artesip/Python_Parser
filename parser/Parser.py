import time
from Adapter import Adapter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_string_by_class_name(driver: webdriver, s: str):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, s))).text


def get_web_element_by_class_name(driver: webdriver, s: str):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, s)))


def get_web_elements_by_class_name(driver: webdriver, s: str):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, s)))


def choose_region(driver: webdriver, s: str):
    choose_button = get_web_element_by_class_name(driver, "UiKitButton_root.UiKitButton_size-l.UiKitButton_variant"
                                                          "-action.UiKitButton_shape-default.UiKitButton_width-full")
    driver.execute_script('arguments[0].click();', choose_button)

    input_field = get_web_element_by_class_name(driver, "AppAddressInput_addressInput.AppAddressInput_modalStyle")
    input_field.send_keys(s)
    input_field.send_keys(Keys.RETURN)
    time.sleep(10)
    accept_button = get_web_element_by_class_name(driver, "UiKitButton_root.UiKitButton_size-m.UiKitButton_variant"
                                                          "-action.UiKitButton_shape-default.DesktopLocationModal_ok")

    driver.execute_script('arguments[0].click();', accept_button)


def parce_elements(driver: webdriver, product_card: list, quotes: list):
    i = 0
    for elem in product_card:
        if i == 7: 
            break
        driver.execute_script('arguments[0].click();', elem)

        quote_name = get_string_by_class_name(driver, "UiKitText_root.UiKitText_Title3.UiKitText_Extrabold"
                                                      ".UiKitText_Text")
        quote_price_now = get_string_by_class_name(driver, "UiKitCorePrice_price.UiKitCorePrice_xl"
                                                           ".UiKitCorePrice_bold.UiKitCorePrice_theme-market-delivery"
                                                           ".UiKitCorePrice_newPrice.UiKitCorePrice_theme-market"
                                                           "-delivery")

        quote_price_old = get_string_by_class_name(driver, "UiKitCorePrice_price.UiKitCorePrice_m"
                                                           ".UiKitCorePrice_medium.UiKitCorePrice_theme-market"
                                                           "-delivery.UiKitCorePrice_oldPrice")
        time.sleep(0.1)

        q_weight = get_string_by_class_name(driver, "UiKitProductFullCard_weight")
        quote_characteristic_title = driver.find_elements(By.CLASS_NAME,
                                                          "UiKitProductCardDescriptions_descriptionTitle")
        quote_characteristic_text = driver.find_elements(By.CLASS_NAME, "UiKitProductCardDescriptions_descriptionText")

        q_exp_d = q_brand = q_made_in = ''

        for i in range(len(quote_characteristic_title)):  # можно переписать легче щас лень
            if q_exp_d != '' and q_brand != '' and q_made_in != '':
                break
            if quote_characteristic_title[i].text == "Срок годности":
                q_exp_d = quote_characteristic_text[i].text
            elif quote_characteristic_title[i].text == "Страна":
                q_made_in = quote_characteristic_text[i].text
            elif quote_characteristic_title[i].text == "Бренд":
                q_brand = quote_characteristic_text[i].text

        quotes.append((Adapter(
            quote_name,
            quote_price_now,
            quote_price_old,
            q_brand,
            q_made_in,
            q_exp_d,
            q_weight
        )))
        close_button = get_web_element_by_class_name(driver,
                                                     "DesktopUIButton_root.ModalCross_button.DesktopUIButton_simple"
                                                     ".DesktopUIButton_sm")
        driver.execute_script('arguments[0].click();', close_button)


def parse(site_path: str):  # requires site path from market-delivery
    all_quotes = []
    site_path_func = site_path
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    driver.get(site_path_func)

    address = "Пермь, улица Попова, 16А"

    choose_region(driver, address)
    time.sleep(10)
    product_card_buttons = driver.find_elements(By.CLASS_NAME, "UiKitDesktopProductCard_root"
                                                               ".UiKitDesktopProductCard_main"
                                                               ".UiKitDesktopProductCard_m"
                                                               ".UiKitDesktopProductCard_fluidWidth"
                                                               ".UiKitDesktopProductCard_clickable")
    parce_elements(driver, product_card_buttons, all_quotes)

    driver.close()
    return list(set(all_quotes))