FROM python:3.11.6-slim-bookworm as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update && apt upgrade -y --no-install-recommends

COPY ./src/requirements.txt .

RUN pip install pip --upgrade && \
    pip install --no-cache-dir -r requirements.txt \
    --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY . /app