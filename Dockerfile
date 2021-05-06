FROM python:3.8-slim-buster

RUN mkdir /app
COPY ./PizzaOrderingService /app/PizzaOrderingService
WORKDIR /app/PizzaOrderingService

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt