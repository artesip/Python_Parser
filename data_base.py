import sqlite3
from sqlite3 import Cursor
import Adapter


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("parser_db.db")
        cur = self.conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS SPECIAL_OFFERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price_now TEXT,
            price_old TEXT,
            brand TEXT,
            made_in TEXT,
            expiration_date TEXT,
            weight TEXT
        )''')

    def insert(self, adapter: Adapter):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO SPECIAL_OFFERS 
            (name, price_now, price_old, brand, made_in, expiration_date, weight) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            adapter.name, adapter.price_now, adapter.price_old,  adapter.brand, adapter.made_in, adapter.expiration_date,
            adapter.weight))
        self.conn.commit()

    def get_special_offers_cursor(self) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM SPECIAL_OFFERS''')
        return cursor

    def __del__(self):
        self.conn.close()
