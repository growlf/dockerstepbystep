FROM python:3-alpine

RUN mkdir -p /var/app_data

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./

EXPOSE 8080
CMD ["python3", "app.py"]
