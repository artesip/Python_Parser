import requests
from flask import Flask
from Config import X5_SITE_PATH, MAGNIT_SITE_PATH
from Parser import parse
from Data_base import DB
import concurrent.futures

app = Flask(__name__)

db = DB()

def do_parse_help(site_path, insert_func):
    try:
        for elem in parse(site_path):
            insert_func(elem)
    except Exception as e:
        print(e)
        return "Parcing went wrong"
    return "Отлично"


@app.route('/pong')
def do_parse():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        magnit_future = executor.submit(do_parse_help, MAGNIT_SITE_PATH, db.insert_into_magnit)
        x5_future = executor.submit(do_parse_help, X5_SITE_PATH, db.insert_into_x5)

        if magnit_future.result() == magnit_future.result() == "Отлично":
            return "Отлично"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
