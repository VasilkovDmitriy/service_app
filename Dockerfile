FROM python:3.9-alpine3.17

RUN adduser --disabled-password service_user
USER service_user

EXPOSE 8000

COPY ./requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY ./service /service
WORKDIR /service
