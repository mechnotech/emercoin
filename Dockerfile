FROM python:3.8.5
LABEL name='Emercoin site' version=1
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .