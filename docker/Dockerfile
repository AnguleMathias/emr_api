FROM python:3.7.4

WORKDIR /app

RUN apt-get update -u && apt-get install -y \
  supervisor \
  netcat

RUN supervisord

COPY emr_api.conf /etc/supervisor/conf.d/emr_api.conf
COPY requirements.txt /app

RUN python3 -m pip install -r requirements.txt && \
  python3 -m pip install alembic && \
  python3 -m pip install gunicorn && \
  python3 -m pip install gevent 