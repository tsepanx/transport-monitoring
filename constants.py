import os
from pathlib import Path

from peewee import *
from yandex_transport_webdriver_api import YandexTransportProxy

from functions import convert


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


class BaseModel(Model):
    class Meta:
        database = MY_DATABASE

    def __str__(self):
        return convert(vars(self)['__data__'])


class RouteData(BaseModel):
    name = CharField()


class ArrivalTime(BaseModel):
    stop_name = CharField()
    way = CharField()
    days = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    arrival_time = TimeField()


class StopData(BaseModel):
    stop_name = CharField()
    way = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    stop_id = IntegerField(null=True)


class ServerTimeFix(BaseModel):
    request_time = TimeField()
    estimated_time = TimeField()


DATABASE_TIMETABLES_LIST = [RouteData, ArrivalTime, StopData, ServerTimeFix]


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
        ways = ("AB", "BA")
        days = ("1111100", "0000011")

        if isinstance(way_filter, str):
            self.way_filter = way_filter
            self.week_filter = week_filter
        else:
            self.way_filter = ways if not way_filter else ways[way_filter]
            self.week_filter = days if not week_filter else days[week_filter]
