FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .



#  RUN poetry config virtualenvs.create false

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
