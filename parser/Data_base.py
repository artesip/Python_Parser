import psycopg2
from Adapter import Adapter


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host="db", database="postgres", user="postgres", password="root")

    def insert(self, adapter: Adapter):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO offers 
            (name_pr, price_now, price_old, brand, made_in, expiration_date, weight_pr) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            adapter.name, adapter.price_now, adapter.price_old, adapter.brand, adapter.made_in, adapter.expiration_date,
            adapter.weight))
        self.conn.commit()

    def get_special_offers_cursor(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM offers")
        self.conn.commit()
        return cursor

    def __del__(self):
        self.conn.close()

    def deleting_all_parsed(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM offers")
        self.conn.commit()

    def get_all_brands(self) -> list:
        cur = self.conn.cursor()
        cur.execute("SELECT brand FROM offers")
        result = set()
        for elem in cur.fetchall():
            result.add(str(elem))
        self.conn.commit()
        return list(result)

    def get_data_by_filter_brand(self, brand_filter: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM offers where brand = %s ", (brand_filter,))
        self.conn.commit()
        return cur