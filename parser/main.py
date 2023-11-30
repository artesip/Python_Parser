import time
import socket
import requests
from flask import Flask
from Parser import parse


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect(('db', 5432))
        s.close
        break
    except socket.error as e:
        time.sleep(0.1) 

from Data_base import DB


app = Flask(__name__)

db = DB()


@app.route('/pong')
def do_parse():
    try:
        for elem in parse():
          db.insert(elem)
    except Exception as e:
        print(e)
        return "Something went wrong"
    return "Отлично"


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = False)
