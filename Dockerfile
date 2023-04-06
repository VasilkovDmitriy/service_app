FROM python:3.9-alpine3.17

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /service

RUN apk add postgresql-client build-base postgresql-dev

COPY ./requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service_user
RUN chown -R service_user:www-data /service/
USER service_user

COPY ./service /service
