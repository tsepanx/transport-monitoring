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

GET_LINE_ID = {
    '732': {
        'line_id': "213_732_bus_mosgortrans",
        'thread_id': "213A_732_bus_mosgortrans",
    }
}

YA_MGT_STOPS_MATCJING = {
    'Давыдковская улица, 12': 'Давыдковская ул., 12'
}


def determine_same_stop_names(ya_name, mgt_name):
    if YA_MGT_STOPS_MATCJING.get(ya_name):
        return YA_MGT_STOPS_MATCJING[ya_name] == mgt_name or ya_name == mgt_name

    else:
        return ya_name == mgt_name


STOP_FIELDS = [
    {
        'stop_id': '9644642',
        'stop_name': 'Давыдковская улица, 12',
    },
    {
        'stop_id': '9640951',
    },
    {
        "stop_id": '9650244'
    }
]
