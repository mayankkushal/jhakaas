
FROM python:3.8

RUN mkdir /app
WORKDIR app

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && pipenv install --deploy --system

COPY . .