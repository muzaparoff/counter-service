FROM python:3.8

RUN pip install flask gevent

COPY counter_service.py /app/counter_service.py

WORKDIR /app

CMD ["python", "counter_service.py"]