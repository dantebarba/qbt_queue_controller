FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ARG BUILD_VERSION=''

ENV BUILD_VERSION ${BUILD_VERSION}
ENV QBT_HOST http://qbittorrent
ENV QBT_PORT 8080
ENV QBT_USERNAME admin
ENV QBT_PASS adminadmin
ENV LOG_LEVEL 'INFO'
ENV LOG_FILE '/var/log/qbt_queue_controller.log'
ENV INTERVAL '15'
ENV TZ 'America/Argentina/Buenos_Aires'

ADD . .

CMD python3 src/main.py
