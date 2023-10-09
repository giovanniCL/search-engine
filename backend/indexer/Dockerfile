FROM python:latest

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

WORKDIR /app

COPY ./db.py /db.py

COPY ./frequencies.py /frequencies.py

COPY ./main.py /main.py

COPY ./start /start

RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

RUN chmod +x /wait

CMD ["/start"]