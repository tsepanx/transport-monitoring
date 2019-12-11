from yandex_transport_webdriver_api import YandexTransportProxy
from functions import *
from constants import *
from peewee import *
from bs4 import BeautifulSoup

import requests
import json
import time
import datetime

db = SqliteDatabase(FILENAMES_PREFIX + MAIN_DB_NAME)
proxy = YandexTransportProxy('127.0.0.1', 25555)


class File:

    def __init__(self, filename, _type="w+"):
        self.full_name = FILENAMES_PREFIX + filename
        self.__file_object = open(self.full_name, _type)
        self.__file_extension = self.full_name.split(".")[1]
        print(self.__file_extension)

    def write(self, data):
        self.__file_object.write(data)

    def write_json(self, data):
        self.__file_object.write(json.dumps(data, indent=4, separators=(',', ': ')))

    def write_csv(self, array_pos):
        for i in range(len(array_pos)):
            self.write(";".join(map(str, [array_pos[i][1], array_pos[i][0], i + 1, i + 1])))
            self.write("\n")

    def read(self):
        return self.__file_object.read()

    def read_json(self):
        return json.loads(self.__file_object.read())

    def get_all_points_list(self):
        return recursive_descent(self.read_json())

    def get_stop_schedules(self):

        data = self.read_json()

        res_dict = dict()

        d = data["data"]["properties"]["StopMetaData"]["Transport"]

        for bus in d:
            name = bus["name"]
            threads = bus["threads"]
            print(name)

            res_dict[name] = dict()

            for thread in threads:
                thread_id = thread["threadId"]
                schedules = thread["BriefSchedule"]
                events = schedules["Events"]

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

                if "Frequency" in schedules:
                    frequency = schedules["Frequency"]["text"]

                    first_arrival = time.localtime(int(schedules["Frequency"]["begin"]["value"]))
                    last_arrival = time.localtime(int(schedules["Frequency"]["end"]["value"]))

                print("id", thread_id, "\n")
                print("times :", *list(map(pretty_time, estimated_times)), sep="\n")
                print("scheduled :", *list(map(pretty_time, scheduled_times)), "\n", sep="\n")
                print("first & last", *list(map(pretty_time, [first_arrival, last_arrival])))
                print("\n")


class Bus:
    paths_list = []
    timetable = {
        ROUTE_AB:
            {WORKDAYS: {}, WEEKENDS: {}},
        ROUTE_BA:
            {WORKDAYS: {}, WEEKENDS: {}}
    }

    def __init__(self, name="0"):
        self.name = name

    def __get_timetable(self, route=ROUTE_AB, days=WORKDAYS, stop_filter="all"):

        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.name}&date={days}&direction={route}&waypoint={stop_filter}"

        request = requests.get(url_string)
        soup = BeautifulSoup(''.join(request.text), features="html.parser")

        stop_names = soup.findAll('h2')[:-1]

        for i in range(len(stop_names)):
            stop_names[i] = stop_names[i].text

        res_dict = dict.fromkeys(stop_names, [])

        if not stop_names:
            return False

        timetable = soup.findAll('table', {'border': '0', 'cellspacing': 0, 'cellpadding': '0'})

        for i in range(1, len(timetable)):
            hours_list = timetable[i].findAll('span', {'class': 'hour'})
            minutes_list = timetable[i].findAll('td', {'align': 'left'})

            output = []
            gray_cnt = 0

            for g in range(len(minutes_list)):
                if minutes_list[g].find('span', {'class': 'minutes'}).text == "":
                    gray_cnt += 1
                    continue
                for j in minutes_list[g].findAll('span', {'class': 'minutes'}):
                    if g - gray_cnt >= len(hours_list):
                        break

                    hours = int(hours_list[g - gray_cnt].text)
                    minutes = int(j.text)

                    output.append(datetime.time(hours, minutes))

            res_dict[stop_names[i - 1]] = output

        self.timetable[route][days] = res_dict

    def __get_stops(self, route=ROUTE_AB, days=WORKDAYS):
        url_string = f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={self.name}&date={days}&direction={route}'
        raw_stops_list = requests.get(url_string)
        stops_list = []
        for stop in raw_stops_list.text.split('\n'):
            if stop != "":
                stops_list.append(stop)

        p = Path(self.name, route, days, stops_list)
        return p

    def get_path(self, route=ROUTE_AB, days=WORKDAYS):
        for i in self.paths_list:
            if i.route == route and i.days == days:
                return i

    def get_all_stops(self, routes=(ROUTE_AB, ROUTE_BA), days=(WORKDAYS, WEEKENDS)):
        try:
            res = []
            for day in days:
                for route in routes:
                    p = self.__get_stops(route, day)
                    res.append(p)
            self.paths_list = res[:]
        except Exception:
            raise Exception("No internet connection")

    def get_all_timetable(self, routes=(ROUTE_AB, ROUTE_BA), days=(WORKDAYS, WEEKENDS)):
        for route in routes:
            for day in days:
                self.__get_timetable(route=route, days=day)


class Path:

    def __init__(self, name, route=ROUTE_AB, days=WORKDAYS, path=()):
        self.name = name
        self.route = route
        self.days = days
        self.stops = path

    def __eq__(self, b):
        return self.stops == b.stops


class Database:

    def __init__(self, db, list):
        self.db = db
        self.list = list
        self.__init_database(list)

    def __init_database(self, path_names, filter_routes=(ROUTE_AB, ROUTE_BA), filter_days=(WORKDAYS, WEEKENDS)):
        self.db.create_tables([BusesDB, Time])

        for i in range(len(path_names)):
            data_source = []

            b = Bus(path_names[i])
            bus = BusesDB.create(name=path_names[i])
            b.get_all_timetable()
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

    def write(self):
        pass  # TODO write rows in to db with peewee

    def read(self):
        pass  # TODO read some info from db


class BusesDB(Model):
    name = CharField()
    bus_class = Bus(name)

    class Meta:
        database = db


class Time(Model):
    stop_name = CharField()
    route = CharField()
    days = CharField()
    bus = ForeignKeyField(BusesDB, related_name="bus")
    arrival_time = TimeField()

    class Meta:
        database = db
