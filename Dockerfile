FROM python:3.11

COPY . /app
WORKDIR /app

RUN apt-get update &&  \
    apt-get install -y sqlite3 &&  \
    pip install --no-cache-dir --upgrade -r requirements.txt