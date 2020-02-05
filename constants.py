import os

from peewee import *
from yandex_transport_webdriver_api import YandexTransportProxy


def create_if_not_exists(path):
    print(path)
    if not os.path.exists(path):
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
        'stop_id': '9644642'}
}


class Tags:
    STOP_NAME = "stopName"

    BRIEF_SCHEDULE = "BriefSchedule"

    STOP_ID = 'stopId'
    THREAD_ID = "threadId"
    LINE_ID = "lineId"

    EVENTS = "Events"

    ESTIMATED = "Estimated"
    SCHEDULED = "Scheduled"

    ESSENTIAL_STOPS = "EssentialStops"

    FREQUENCY = "Frequency"

    STOP_META_DATA = "StopMetaData"
    PROPERTIES = "properties"
