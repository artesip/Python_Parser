import requests
from Config import PARSE_SERVICE
from flask import Flask
from Data_base import DB

db = DB()


async def parce_site() -> str:
    db.deleting_all_parsed_magnit()
    db.deleting_all_parsed_x5()
    response = ''
    try:
        response = requests.get(f'http://{PARSE_SERVICE}:5001/pong', timeout=1200)
    except requests.exceptions.RequestException as e:
        s = '\n Cannot reach the parse service.'
        print(s)
        return s

    return "Сайт успешно спарсен! " + response.text


async def deleting_all_parsed() -> str:
    try:
        db.deleting_all_parsed_magnit()
        db.deleting_all_parsed_x5()
    except Exception as e:
        print(e)
        return "Something went wrong mb it is empty"

    return "All  deleted"


async def get_all_brands_x5():
    try:
        return db.get_all_brands_x5()
    except Exception as e:
        print(e)
        return "Something went wrong"


async def get_all_brands_magnit():
    try:
        return db.get_all_brands_magnit()
    except Exception as e:
        print(e)
        return "Something went wrong"


async def get_x5_items_by_filter_brand(brand: str):
    try:
        return db.get_data_x5_by_filter_brand(brand)
    except Exception as e:
        print(e)
        return "Something went wrong"


async def get_magnit_items_by_filter_brand(brand: str):
    try:
        return db.get_data_magnit_by_filter_brand(brand)
    except Exception as e:
        print(e)
        return "Something went wrong"
