import os
import peewee as pw
from yandex_transport_webdriver_api import YandexTransportProxy

GENERATED_DIR = "static/"
PROJECT_PREFIX = os.path.dirname(__file__) + "/"

DATABASE_PATH = PROJECT_PREFIX + "buses.db"
MY_DATABASE = pw.SqliteDatabase(DATABASE_PATH)

# myDB = pw.MySQLDatabase("mydb", host="...", port=3306, user="user",
#                         passwd="password")

PROXY_CONNECT_TIMEOUT = 5

GET_LINE_ID = {
    '732': {
        'line_id': "213_732_bus_mosgortrans",
        'thread_id': "213A_732_bus_mosgortrans",
    }
}

STOP_FIELDS = [
    {
        'stop_id': '9644642',
        'stop_name': 'Давыдковская улица, 12',
    },
    {'stop_id': '9640951'}, {"stop_id": '9650244'}
]
MAX_QUERY_ITERATIONS = float('inf')
DEFAULT_TIMEOUT = 30
MIN_TIMEOUT = 10
proxy = YandexTransportProxy('127.0.0.1', 25555)