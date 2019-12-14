import enum
import os
from peewee import *

FILENAMES_PREFIX = "generated_files/"
PROJECT_PREFIX = os.getcwd() + "/"

if not os.path.exists(PROJECT_PREFIX + FILENAMES_PREFIX):
    os.mkdir(PROJECT_PREFIX + FILENAMES_PREFIX)

JSON_LINE_PREFIX = "line_"
JSON_STOP_PREFIX = "stop_"

# MAIN_BUS_NAME = "732"
MAIN_DB_FILENAME = "buses.db"  # MAIN_BUS_NAME + ".db"

DB = SqliteDatabase(MAIN_DB_FILENAME)

LINE_ID_732 = "213_732_bus_mosgortrans"
THREAD_ID_732 = "213A_732_bus_mosgortrans"

BUSES_LIST = ["27", "104", "732"]

STOP_732_ID = 9644642  # Давыдковская улица, 10
STOP_641_ID = 9644493
STOP_434_ID = 10110344

STOPS_ID = {
    "732": STOP_732_ID,
    "641": STOP_641_ID,
    "434": STOP_434_ID,
}


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


class TimetableFilter:
    WORKDAYS = "1111100"
    WEEKENDS = "0000011"
    ROUTE_AB = "AB"
    ROUTE_BA = "BA"

    ROUTES = (ROUTE_AB, ROUTE_BA)
    DAYS = (WORKDAYS, WEEKENDS)
