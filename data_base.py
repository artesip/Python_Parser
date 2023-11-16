import sqlite3
from sqlite3 import Cursor
from parser import Adapter


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("parser_db.db")
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS SPECIAL_OFFERS')
        cur.execute('''
        CREATE TABLE SPECIAL_OFFERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price_old REAL,
            price_now REAL,
            brand TEXT,
            made_in TEXT,
            expiration_date TEXT,
            weight REAL
        )''')

    def insert(self, adapter: Adapter):
        cursor = self.conn.cursor()
        cursor.execute(f'''INSERT INTO SPECIAL_OFFERS (name, price_old, price_now, brand, made_in, expiration_date,
                                                                                                        weight) VALUES 
                       ('{adapter.name}', '{adapter.price_old}', '{adapter.price_now}', '{adapter.brand}',
                        '{adapter.made_in}', '{adapter.expiration_date}', '{adapter.weight}')
        ''')

    def get_special_offers_cursor(self) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM SPECIAL_OFFERS''')
        return cursor

    def __del__(self):
        self.conn.commit()
        self.conn.close()
