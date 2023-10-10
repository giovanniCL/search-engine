FROM python:latest

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

WORKDIR /app

COPY . /app

RUN sed -i 's/\r$//g' /app/start
RUN chmod +x /app/start

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

RUN chmod +x /wait

CMD ["/app/start"]