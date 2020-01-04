import enum
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


class RouteData(Model):
    name = CharField()

    class Meta:
        database = MY_DATABASE


class ArrivalTime(Model):
    stop_name = CharField()
    way = CharField()
    days = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    arrival_time = TimeField()

    class Meta:
        database = MY_DATABASE


class StopData(Model):
    stop_name = CharField()
    way = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    stop_id = IntegerField(null=True)

    class Meta:
        database = MY_DATABASE


class ServerTimeFix(Model):
    request_time = TimeField()
    estimated_time = TimeField()

    class Meta:
        database = MY_DATABASE


DATABASE_TIMETABLES_LIST = [RouteData, ArrivalTime, StopData, ServerTimeFix]


class Request(enum.Enum):
    GET_STOP_INFO = {'func': proxy.get_stop_info, 'prefix': 'stop_'}
    GET_LINE = {'func': proxy.get_line, 'prefix': 'line_'}


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
    def __init__(self, way_filter: int = None, week_filter: int = None):
        ways = ("AB", "BA")
        days = ("1111100", "0000011")

        self.way_filter = ways if not way_filter else ways[way_filter]
        self.week_filter = days if not week_filter else days[week_filter]
