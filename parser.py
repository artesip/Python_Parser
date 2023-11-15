import urllib.request
from bs4 import BeautifulSoup
import re


class Adapter:
    def __init__(self, name: str, price_now: str, price_old: str):
        self.name = name
        self.price_now = price_now
        self.price_old = price_old


def clear_string(s: str) -> str:
    elems = ['\n', '\t']
    for elem in elems:
        temp = s.split(elem)
        s = ''
        s = ''.join(temp)
        s = re.sub(" +", " ", s)

    if s[-3] == '.' and s[-4] == ' ':
        temp = s[-2] + s[-1]
        s = s[0:-4] + '.' + temp
    elif s[-5] == '.' and s[-6] == ' ':
        temp = s[-3] + s[-2]
        s = s[0:-6] + '.' + temp

    return s


def parse() -> list:
    all_quotes = []
    request = urllib.request.urlopen(f'https://5ka.ru/special_offers')
    html = request.read()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_quotes = bsObj.find_all('div', {'class': 'product-card item'})

    for found_quote in found_quotes:
        quote_price_now = found_quote.find('span', {'data-v-2d064667': ''}).text
        quote_price_now_cents = found_quote.find('span', {'class': 'price-discount_cents'}).text
        quote_price_old = found_quote.find('span', {'class': 'price-regular'}).text
        quote_name = found_quote.find('div', {'class': 'item-name'}).text

        all_quotes.append(Adapter(
            clear_string(quote_price_now + '.' + quote_price_now_cents)[3:-1],
            clear_string(quote_price_old)[1:],
            clear_string(quote_name)[5:]
        ))
    return all_quotes
