FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/list/*

WORKDIR /app

COPY ./task_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./task_app /app

EXPOSE 8000