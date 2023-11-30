FROM gherman/python-selenium-firefox

COPY . .

RUN pip install psycopg2
RUN pip install Flask
RUN pip install requests

CMD ["python", "main.py"]