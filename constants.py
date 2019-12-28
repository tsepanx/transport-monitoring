import enum
import os
from peewee import *

from pathlib import Path

from yandex_transport_webdriver_api import YandexTransportProxy

FILENAMES_PREFIX = "generated_files/"
PROJECT_PREFIX = str(Path.home()) + "/TransportMonitoring/"

proxy = YandexTransportProxy('127.0.0.1', 25555)

if not os.path.exists(PROJECT_PREFIX + FILENAMES_PREFIX):
    print(PROJECT_PREFIX)
    os.mkdir(PROJECT_PREFIX + FILENAMES_PREFIX)

MAIN_DB_PATH = PROJECT_PREFIX + "buses.db"

GLOBAL_DB = SqliteDatabase(MAIN_DB_PATH)

PROXY_CONNECT_TIMEOUT = 5

SHORT_STOP_ID_LENGTH = 7
LONG_STOP_ID_LENGTH = 10
#
# STOP_732_ID = 9644642  # Давыдковская улица, 10
# STOP_641_ID = 9644493
# STOP_434_ID = 10110344

routes_fields = {
    '732': {
        'line_id': "213_732_bus_mosgortrans",
        'thread_id': "213A_732_bus_mosgortrans",
        'main_stop_id': '9644642'}
}


class RouteData(Model):
    name = CharField()

    class Meta:
        database = GLOBAL_DB


class ArrivalTime(Model):
    stop_name = CharField()
    way = CharField()
    days = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    arrival_time = TimeField()

    class Meta:
        database = GLOBAL_DB


class StopData(Model):
    stop_name = CharField()
    way = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    stop_id = IntegerField(null=True)

    class Meta:
        database = GLOBAL_DB


class ServerTimeFix(Model):
    request_time = TimeField()
    estimated_time = TimeField()

    class Meta:
        database = GLOBAL_DB


DATABASE_TIMETABLES_LIST = [RouteData, ArrivalTime, StopData, ServerTimeFix]


class Request(enum.Enum):
    GET_STOP_INFO = "stop_"
    GET_LINE = "line_"


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


class Filters:
    def __init__(self, way_filter: int = None, week_filter: int = None):
        ways = ("AB", "BA")
        days = ("1111100", "0000011")

        self.way_filter = ways if not way_filter else ways[way_filter]
        self.week_filter = days if not week_filter else days[week_filter]

        # self.all_args = {
        #     'ways': self.WAYS,
        #     'days': self.DAYS
        # }
