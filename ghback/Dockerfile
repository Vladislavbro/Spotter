# syntax=docker/dockerfile:1
FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m spacy download ru_core_news_md
RUN apt-get -y update
RUN apt-get -y upgrade
COPY . /code/
