from python_parse import parser
from python_parse import data_base as DB
from pymongo import MongoClient
from pprint import pprint

def parce_and_add_to_bd(local_db:DB):
    for elem in parse():
        local_db.insert(elem)


if __name__ == '__main__':
        '''
        db = DB()
        while(True):

            print("What you to do ? \n1. Get to DB all offers. \n2. Print all offers. \n3. Try to find by filters. "
                  "\nOther. Exit and save. ")
            temp = input()

            if temp == '1':
                parce_and_add_to_bd(db)
            elif temp == '2':
                cursor = db.get_special_offers_cursor()
                for elem in cursor.fetchall():
                    print(elem)
                print()
            else:
                break
        '''
        Mongo_URL = "mongodb://mongo:27017"
        client = MongoClient(Mongo_URL)
        db = client.admin
        db.list = db.command("listDatabases")

        print("doker-compose working")
