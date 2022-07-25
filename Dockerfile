FROM python:3.8-slim-buster
MAINTAINER Pyae Phyo Kyaw

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app