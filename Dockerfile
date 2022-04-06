# syntax=docker/dockerfile:1

FROM python:3.8

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
    && apt-get -y update\
    && apt-get install -y wget \
    && apt-get install -y google-chrome-stable 

WORKDIR ./app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .


