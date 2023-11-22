from Parser import parse
from Data_base import DB

db = DB()


async def parce_site() -> str:
    try:
        for elem in await parse():
            db.insert(elem)
    except Exception as e:
        print(e)
        return Something went wrong
    return "Сайт успешно спарсен! "


async def deleting_all_parsed() -> str:
    try:
        db.deleting_all_parsed()
    except Exception as e:
        print(e)
        return "Something went wrong mb it is empty"

    return "All  deleted"


async def get_all_brands():
    try:
        return db.get_all_brands()
    except Exception as e:
        print(e)
        return "Something went wrong"


async def get_items_by_filter_brand(brand: str):
    try:
        return db.get_data_by_filter_brand(brand)
    except Exception as e:
        print(e)
        return "Something went wrong"
