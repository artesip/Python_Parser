FROM python

COPY . .
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

RUN pip install Flask
RUN pip install aiogram
RUN pip install psycopg2
RUN pip install requests
RUN chmod +x ./start.sh

CMD /wait && /start.sh
