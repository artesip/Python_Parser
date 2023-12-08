FROM gherman/python-selenium-firefox

COPY . .
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

RUN pip install psycopg2
RUN pip install Flask
RUN pip install requests

CMD /wait && bash /start.sh
