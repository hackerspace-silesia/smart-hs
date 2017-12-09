import urllib.request
import json
import os


from influxdb import InfluxDBClient


DATA_URL = "https://hs-silesia.pl/esp12.txt"


def get_data():
    with urllib.request.urlopen(DATA_URL) as data:
        readings = data.read()
    return json.loads(readings.decode("utf8"))


def push_readings(readings):
    body = [
        {
            "measurement": "humidity",
            "tags": {
                "room": "meeting",
            },
            "fields": {
                "value": readings['dht_hum']
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "room": "meeting",
            },
            "fields": {
                "value": readings['bmp_temp']
            }
        },
        {
            "measurement": "presure",
            "tags": {
                "room": "meeting",
            },
            "fields": {
                "value": readings['bmp_press'] / 100
            }
        },
        {
            "measurement": "luminosity",
            "tags": {
                "room": "meeting",
            },
            "fields": {
                "value": readings['lum']
            }
        },
    ]
    get_client().write_points(body)


def get_client():
    ip = os.getenv("INFLUX_ADDRESS")
    port = os.getenv("INFLUX_PORT")
    user = os.getenv("INFLUX_USER")
    password = os.getenv("INFLUX_PASSWORD")
    db = os.getenv("INFLUX_DB")
    return InfluxDBClient(ip, port, user, password, db)


def init():
    db = os.getenv("INFLUX_DB")
    get_client().create_database(db)


if __name__ == '__main__':
    init()
    push_readings(get_data())
