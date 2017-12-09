FROM python:3.5-alpine

RUN pip install influxdb

COPY weather.py weather.py

CMD ["python", "weather.py"]
