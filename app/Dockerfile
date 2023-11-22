FROM gherman/python-selenium-firefox

COPY . .

RUN pip install selenium
RUN pip install pymongo
RUN pip install aiogram

CMD ["python", "main.py"]