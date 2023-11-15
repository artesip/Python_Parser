from parser import parse
from data_base import DB
from data_base import Cursor


def print_all_db(cur: Cursor):
    print(cur.fetchall())


def main_start():
    for elem in parse():
        db.insert(elem)
    print_all_db(db.get_special_offers_cursor())


if __name__ == '__main__':

    try:

        db = DB()
        main_start()

    except:
        print("Something went wrong!")
