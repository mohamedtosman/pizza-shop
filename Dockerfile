FROM python:3.7-alpine

RUN apk add --update --no-cache postgresql-dev gcc python3-dev musl-dev

WORKDIR /code

COPY requirements.txt requirements-dev.txt ./

RUN pip install --upgrade pip && pip install pylint-django && pip install -r requirements-dev.txt
