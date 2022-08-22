FROM python:3.9 
WORKDIR /usr/app/src
COPY main.py ./
COPY requirements.txt ./
COPY helper_functions ./
COPY schema.xsd ./
RUN pip install -r requirements.txt