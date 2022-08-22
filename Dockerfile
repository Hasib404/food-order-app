FROM python:3.9-slim-buster
WORKDIR /usr/app/src
COPY main.py ./
COPY requirements.txt ./
COPY helper_functions.py ./
COPY schema.xsd ./
RUN pip install -r requirements.txt