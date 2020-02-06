import os

from peewee import *
from yandex_transport_webdriver_api import YandexTransportProxy


def does_exist(path):
    return os.path.exists(path)


def create_if_not_exists(path):
    print(path)
    if not does_exist(path):
        print('Creating ', path)
        os.mkdir(path)


def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def get_full_filename(filename, ext="json"):
    return PROJECT_PREFIX + GENERATED_DIR + filename + "." + ext


proxy = YandexTransportProxy('127.0.0.1', 25555)

GENERATED_DIR = "generated_files/"
PROJECT_PREFIX = os.path.dirname(__file__) + "/"
create_if_not_exists(PROJECT_PREFIX + GENERATED_DIR)

DATABASE_PATH = PROJECT_PREFIX + "buses.db"

MY_DATABASE = SqliteDatabase(DATABASE_PATH)

PROXY_CONNECT_TIMEOUT = 5

ROUTES_FIELDS = {
    '732': {
        'line_id': "213_732_bus_mosgortrans",
        'thread_id': "213A_732_bus_mosgortrans",
    }
}

TEST_FIELDS = {
    'stop_id': '9644642',
    'stop_name': 'Давыдковская улица, 12',
}
