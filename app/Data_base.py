import psycopg2
from Adapter import Adapter
from Config import HOST, DATABASE, USER, PASSWORD


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

    def insert_into_id(self, id):
        try:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users_id
            (user_id) 
            VALUES (%s)
        ''', [id])
        self.conn.commit()
        except Exception as e:
            print(e)

    def insert_into_x5(self, adapter: Adapter):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO offers_x5
            (name_pr, price_now, price_old, brand, made_in, expiration_date, weight_pr) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            adapter.name, adapter.price_now, adapter.price_old, adapter.brand, adapter.made_in, adapter.expiration_date,
            adapter.weight))
        self.conn.commit()

    def insert_into_magnit(self, adapter: Adapter):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO offers_magnit
            (name_pr, price_now, price_old, brand, made_in, expiration_date, weight_pr) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            adapter.name, adapter.price_now, adapter.price_old, adapter.brand, adapter.made_in, adapter.expiration_date,
            adapter.weight))
        self.conn.commit()


    def get_user_id_cursor(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users_id")
        self.conn.commit()
        return cursor


    def get_special_offers_x5_cursor(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM offers_x5")
        self.conn.commit()
        return cursor

    def get_special_offers_magnit_cursor(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM offers_magnit")
        self.conn.commit()
        return cursor

    def deleting_all_parsed_x5(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM offers_x5")
        self.conn.commit()

    def deleting_all_parsed_magnit(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM offers_magnit")
        self.conn.commit()

    def get_all_brands_x5(self) -> list:
        cur = self.conn.cursor()
        cur.execute("SELECT brand FROM offers_x5")
        result = set()
        for elem in cur.fetchall():
            result.add(str(elem))
        self.conn.commit()
        return list(result)

    def get_all_brands_magnit(self) -> list:
        cur = self.conn.cursor()
        cur.execute("SELECT brand FROM offers_magnit")
        result = set()
        for elem in cur.fetchall():
            result.add(str(elem))
        self.conn.commit()
        return list(result)

    def get_data_x5_by_filter_brand(self, brand_filter: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM offers_x5 where brand = %s ", (brand_filter,))
        self.conn.commit()
        return cur

    def get_data_magnit_by_filter_brand(self, brand_filter: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM offers_magnit where brand = %s ", (brand_filter,))
        self.conn.commit()
        return cur

    def __del__(self):
        self.conn.close()
