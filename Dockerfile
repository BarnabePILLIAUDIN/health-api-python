FROM python:3.9-slim

COPY ./src  /app/src
COPY requirements.txt /app
COPY .env /app/.env

RUN pip install -r /app/requirements.txt

CMD ["python3", "/app/src/app.py"]