import datetime
import json
import time

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
    with open(filename, "r") as file:
        data = json.loads(file.read())

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
    fout = open(filename, "w")
    for i in range(len(pos_arr)):
        fout.write(";".join(map(str,
                                [pos_arr[i][1], pos_arr[i][0], i + 1, i + 1]
                                )))
        fout.write("\n")


def write_data_to_file(func, filename, url):
    print("---Requesting data---")
    data = func(url)
    print(data)
    with open(filename, 'w') as fout:
        fout.write(json.dumps(data, indent=4, separators=(',', ': ')))


def get_stop_url(id):
    return "https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__" + str(id)


def get_line_url(id, thread_id):
    return f"https://yandex.ru/maps/213/moscow/?ll=37.679549,55.772203&masstransit[lineId]={id}&masstransit[threadId]={thread_id}&mode=stop&z=18"


def make_url_with_position(coords):
    s = f"https://yandex.ru/maps/213/moscow/?ll=37.634438%2C55.741204&mode=search&sll=37.633301%2C55.743449&sspn=0.009463%2C0.003159&text={coords[0]},{coords[1]}&z=14"
    return s


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
    with open(filename, "r") as file:
        data = json.loads(file.read())
    return recursive_descent(data)


def init_database(raw_buses_list, filter_routes=(ROUTE_AB, ROUTE_BA), filter_days=(WORKDAYS, WEEKENDS)):
    db.create_tables([BusesDB, Time])

    for i in range(len(raw_buses_list)):
        data_source = []

        b = Bus(raw_buses_list[i])
        bus = BusesDB.create(name=raw_buses_list[i])
        b.get_timetable()
        for route in b.timetable:
            for day in b.timetable[route]:
                for stop_name in b.timetable[route][day]:
                    for time in b.timetable[route][day][stop_name]:
                        print(b.name, route, day, stop_name, time)
                        data_source.append((stop_name, bus, time, route, day))

        Time.insert_many(data_source, fields=[
            Time.stop_name,
            Time.bus,
            Time.arrival_time,
            Time.route,
            Time.days]).execute()


def is_today_weekend():
    day = datetime.date.today().weekday()
    return day in [5, 6]


def pretty_time(time_struct):
    return ":".join(map(str, [time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec]))