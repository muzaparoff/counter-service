FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/counter_service.py

EXPOSE 80

CMD ["python", "counter_service.py"]