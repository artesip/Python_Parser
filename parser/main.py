import requests
from flask import Flask
from Config import X5_SITE_PATH, MAGNIT_SITE_PATH
from Parser import parse
from Data_base import DB

app = Flask(__name__)

db = DB()


@app.route('/pong')
def do_parse():
    try:
        for elem in parse(MAGNIT_SITE_PATH):
            db.insert_into_magnit(elem)
    except Exception as e:
        print(e)
        return "Parcing Magnit went wrong"
    try:
        for elem in parse(X5_SITE_PATH):
            db.insert_into_x5(elem)
    except Exception as e:
        print(e)
        return "Parcing x5 went wrong"

    return "Отлично"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
