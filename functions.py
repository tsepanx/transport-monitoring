import datetime
import json
import time
import classes as c

from peewee import *
from yandex_transport_webdriver_api import YandexTransportProxy

WORKDAYS = "1111100"
WEEKENDS = "0000011"
ROUTE_AB = "AB"
ROUTE_BA = "BA"

FILENAMES_PREFIX = "generated_files/"

db = SqliteDatabase(FILENAMES_PREFIX + 'db_641.db')
proxy = YandexTransportProxy('127.0.0.1', 25555)


def get_stop_schedules(filename):

    data = c.File(filename, "r").read_json()

    res_dict = dict()

    d = data["data"]["properties"]["StopMetaData"]["Transport"]

    for bus in d:
        name = bus["name"]
        threads = bus["threads"]
        print(name)

        res_dict[name] = dict()

        for thread in threads:
            thread_id = thread["threadId"]
            shedules = thread["BriefSchedule"]
            events = shedules["Events"]

            estimated_times = []
            scheduled_times = []

            for event in events:
                if "Estimated" in event:
                    x = int(event["Estimated"]["value"])

                    time_estimated = time.localtime(x)
                    estimated_times.append(time_estimated)
                else:
                    x = int(event["Scheduled"]["value"])

                    time_scheduled = time.localtime(x)
                    scheduled_times.append(time_scheduled)

            if "Frequency" in shedules:
                frequency = shedules["Frequency"]["text"]

                first_arrival = time.localtime(int(shedules["Frequency"]["begin"]["value"]))
                last_arrival = time.localtime(int(shedules["Frequency"]["end"]["value"]))

            print("id", thread_id, "\n")
            print("times :", *list(map(pretty_time, estimated_times)), sep="\n")
            print("scheduled :", *list(map(pretty_time, scheduled_times)), "\n", sep="\n")
            print("first & last", *list(map(pretty_time, [first_arrival, last_arrival])))
            print("\n")


def write_csv_file(filename, pos_arr):
    file = c.File(filename)
    for i in range(len(pos_arr)):
        file.file_object.write(";".join(map(str,
                                [pos_arr[i][1], pos_arr[i][0], i + 1, i + 1]
                                )))
        file.file_object.write("\n")


def get_stop_url(id):
    return "https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__" + str(id)


def get_line_url(id, thread_id):
    return f"https://yandex.ru/maps/213/moscow/?ll=37.679549,55.772203&masstransit[lineId]={id}&masstransit[threadId]={thread_id}&mode=stop&z=18"


def recursive_descent(data):
    res = []
    cur = []

    if type(data) == type(dict()):
        for i in data:
            cur.append(data[i])
    else:
        cur = data

    if len(cur) == 2:
        if list(map(type, cur)) == [type(float())] * 2:
            return [cur]

    for x in cur:
        if type(x) in [type([]), type(dict())]:
            z = recursive_descent(x)
            res.extend(z)

    return res


def get_all_coordinates_from_file(filename):
    return recursive_descent(c.File(filename, "r").read_json())


def is_today_weekend():
    day = datetime.date.today().weekday()
    return day in [5, 6]


def pretty_time(time_struct):
    return ":".join(map(str, [time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec]))
