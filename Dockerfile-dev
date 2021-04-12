FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir -p app/api

WORKDIR /app

COPY ./requirements.txt /app

COPY ./api /app/api

RUN pip install --upgrade pip && pip install -r requirements.txt


