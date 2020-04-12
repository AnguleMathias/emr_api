FROM python:3.7.4

WORKDIR /app

RUN apt-get update -u && apt-get install -y \
  supervisor \
  netcat

RUN supervisord

COPY emr_api.conf /etc/supervisor/conf.d/emr_api.conf
COPY requirements.txt /app

RUN pip install -r requirements.txt && pip install gevent