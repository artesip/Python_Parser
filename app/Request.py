from Adapter import Adapter
import requests
from collections import defaultdict
from flask import Flask
from Data_base import DB
from Config import PARSE_SERVICE


db = DB()

async def instert_id(user_id):
    db.insert_into_id(user_id)

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
    if response.text != "Отлично":
        return "Произошла ошибка попробуйте еще раз"
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

async def get_2store_dicts():
    dict_magnit = defaultdict(list)
    dict_x5 = defaultdict(list)

    cursor = db.get_special_offers_x5_cursor()

    for elem in cursor.fetchall():
        dict_x5[elem[4]].append(Adapter(elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))

    cursor = db.get_special_offers_magnit_cursor()
    for elem in cursor.fetchall():
        dict_magnit[elem[4]].append(Adapter(elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))
    
    return (dict_x5, dict_magnit)