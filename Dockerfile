FROM python:3.10.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements2.txt

EXPOSE 8000