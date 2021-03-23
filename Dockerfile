FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt


# ADD api /app/api

# RUN mkdir -p /app/api/email-templates/build

# EXPOSE 80

WORKDIR /app
COPY . /app/

# ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
    
    