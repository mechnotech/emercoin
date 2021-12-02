FROM python:3.10.0-slim-buster
LABEL name='Emercoin site' version=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .