import os
from pathlib import Path

from peewee import *
from yandex_transport_webdriver_api import YandexTransportProxy


def create_if_not_exists(path):
    if not os.path.exists(path):
        print('Creating ', path)
        os.mkdir(path)


def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def get_full_filename(filename, ext="json"):
    return PROJECT_PREFIX + GENERATED_DIR + filename + "." + ext


GENERATED_DIR = "generated_files/"
PROJECT_PREFIX = str(Path.home()) + "/TransportMonitoring/"

proxy = YandexTransportProxy('127.0.0.1', 25555)

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
    THREAD_ID = "threadId"
    LINE_ID = "lineId"

    EVENTS = "Events"

    ESTIMATED = "Estimated"
    SCHEDULED = "Scheduled"

    ESSENTIAL_STOPS = "EssentialStops"

    FREQUENCY = "Frequency"

    STOP_META_DATA = "StopMetaData"
    PROPERTIES = "properties"


class Filter:
    def __init__(self, way_filter=None, week_filter=None):
        self.ways = ("AB", "BA")
        self.days = ("1111100", "0000011")

        if isinstance(way_filter, str):
            self.way_filter = [way_filter]
        else:
            self.way_filter = self.ways if way_filter is None else [self.ways[way_filter]]

        if isinstance(week_filter, str):
            self.week_filter = [week_filter]
        else:
            self.week_filter = self.days if week_filter is None else [self.days[week_filter]]
