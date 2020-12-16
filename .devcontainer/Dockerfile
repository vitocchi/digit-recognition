FROM python:3.6-slim

    
RUN apt-get update \
    && echo 'deb https://notesalexp.org/tesseract-ocr/buster/ buster main' >> /etc/apt/sources.list \
    && apt-get update -oAcquire::AllowInsecureRepositories=true \
    && apt-get install -y notesalexp-keyring --allow-unauthenticated -oAcquire::AllowInsecureRepositories=true \
    && apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated \
    apt-utils \
    gcc \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    && pip install --no-cache-dir \
    autopep8 \
    flake8 \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
