from parser import parse
from data_base import DB


def parce_and_add_to_bd(local_db:DB):
    for elem in parse():
        local_db.insert(elem)


if __name__ == '__main__':

    try:
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

    except:
        print("Something went wrong!")
