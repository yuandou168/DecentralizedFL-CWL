# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /files


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir


COPY . .
EXPOSE 8008
ENTRYPOINT [ "python", "flask_endpoint_discovery.py"]

