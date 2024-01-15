# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /files

ADD requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip3 pip3 install -r requirements.txt --no-cache-dir

# COPY ./requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt --no-cache-dir


COPY . .
EXPOSE 8008
ENTRYPOINT [ "python", "flask_endpoint_discovery.py"]

