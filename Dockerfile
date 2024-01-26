# Dockerfile
FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

CMD celery -A app worker --loglevel=info