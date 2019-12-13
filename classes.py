from functions import *
from deprecation import *
from yandex_transport_webdriver_api import YandexTransportProxy
from bs4 import BeautifulSoup

import requests
import json
import time
import datetime

proxy = YandexTransportProxy('127.0.0.1', 25555)


class File:

    def __init__(self, filename, is_already_created=True):
        self.full_name = FILENAMES_PREFIX + filename
        self.__file_extension = self.full_name.split(".")[1]

        self.__open("r" if is_already_created else "w+")
        print(self.full_name, self.__file_extension)

    def __open(self, _type):
        self.__file_object = open(self.full_name, _type)

    def __write(self, data):
        self.__open("w")
        self.__file_object.write(data)

    def write_json(self, data):
        self.__write(json.dumps(data, indent=4, separators=(',', ': ')))

    def write_csv(self, array_pos):
        for i in range(len(array_pos)):
            self.__write(";".join(map(str, [array_pos[i][1], array_pos[i][0], i + 1, i + 1])))
            self.__write("\n")

    def __read(self):
        self.__open("r")
        return self.__file_object.read()

    def read_json(self):
        return json.loads(self.__read())

    def get_all_points_list(self):
        return recursive_descent(self.read_json())

    def get_stop_schedules(self):
        data = self.read_json()

        res_dict = dict()

        props = data["data"]["properties"]
        stop_russian_fullname = props["name"]
        transport_data = props["StopMetaData"]["Transport"]

        res_dict[Tags.STOP_NAME] = stop_russian_fullname

        for bus in transport_data:
            if bus["type"] != "bus":
                continue

            print(__name__)
            name = bus["name"]
            line_id = bus[Tags.LINE_ID]

            res_dict[name] = {
                Tags.LINE_ID: line_id,
                Tags.THREAD_ID: [],

                Tags.SCHEDULED: [],
                Tags.ESTIMATED: [],
                Tags.FREQUENCY: None,

                Tags.ESSENTIAL_STOPS: []
            }

            threads = bus["threads"]

            for thread in threads:
                thread_id = thread[Tags.THREAD_ID]
                schedules = thread[Tags.BRIEF_SCHEDULE]
                events = schedules[Tags.EVENTS]

                res_dict[name][Tags.THREAD_ID].append(thread_id)

                for event in events:
                    for tag in event:
                        if tag != "vehicleId":
                            value = time.localtime(int(event[tag]["value"]))
                            res_dict[name][tag].append(convert_time(value))

                if Tags.FREQUENCY in schedules:
                    frequency = schedules[Tags.FREQUENCY]["value"] // 60

                    first_arrival = time.localtime(int(schedules[Tags.FREQUENCY]["begin"]["value"]))
                    last_arrival = time.localtime(int(schedules[Tags.FREQUENCY]["end"]["value"]))

                    res_dict[name][Tags.FREQUENCY] = frequency
                    res_dict[name][Tags.ESSENTIAL_STOPS] = [convert_time(first_arrival), convert_time(last_arrival)]

        return res_dict


class Bus:
    paths_list = []
    timetable = {
        TimetableFilter.ROUTE_AB:
            {TimetableFilter.WORKDAYS: {}, TimetableFilter.WEEKENDS: {}},
        TimetableFilter.ROUTE_BA:
            {TimetableFilter.WORKDAYS: {}, TimetableFilter.WEEKENDS: {}}
    }

    def __init__(self, name="0"):
        self.name = name

    @deprecated("Use __get_timetable instead")
    def get_stops(self, route=TimetableFilter.ROUTE_AB, days=TimetableFilter.WORKDAYS):
        url_string = f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={self.name}&date={days}&direction={route}'
        print(url_string)
        
        raw_stops_list = requests.get(url_string)
        stops_list = []
        for stop in raw_stops_list.text.split('\n'):
            if stop != "":
                stops_list.append(stop)

        return stops_list

    @deprecated("Use get_all_timetable instead")
    def get_all_stops(self, routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA), days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS)):
        try:
            res = []
            for day in days:
                for route in routes:
                    p = self.get_stops(route, day)
                    res.append(p)
            self.paths_list = res[:]
        except Exception:
            raise Exception("No internet connection")

    def get_timetable(self, route=TimetableFilter.ROUTE_AB, days=TimetableFilter.WORKDAYS, stop_filter="all"):

        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.name}&date={days}&direction={route}&waypoint={stop_filter}"

        request = requests.get(url_string)
        soup = BeautifulSoup(''.join(request.text), features="html.parser")

        stop_names = soup.findAll('h2')[:-1]

        for i in range(len(stop_names)):
            stop_names[i] = stop_names[i].text

        res_dict = dict.fromkeys(stop_names, [])

        # print(url_string)

        if not stop_names:
            raise Exception("NULL timetable got \n" + url_string)

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
        return self.timetable[route][days]

    def get_all_timetable(self, routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA), days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS)):
        for route in routes:
            for day in days:
                self.get_timetable(route=route, days=day)


class Database:

    def __init__(self, db, list, _filter_routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA), _filter_days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS)):
        self.db = db
        self.list = list
        self.__init_database(list, filter_routes=_filter_routes, filter_days=_filter_days)

    def __init_database(self, bus_names, filter_routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA), filter_days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS)):
        self.db.create_tables([BusesDB, TimetableDB, StopsDB])

        for i in range(len(bus_names)):
            time_data_source = []
            stop_data_source = []

            b = Bus(bus_names[i])
            b.get_all_timetable(routes=filter_routes, days=filter_days)

            bus_row = BusesDB.create(name=bus_names[i])

            for route in b.timetable:
                for day in b.timetable[route]:
                    for stop_name in b.timetable[route][day]:
                        stop_data_source.append(
                            (stop_name,
                             route,
                             bus_row))

                        for arrival_time in b.timetable[route][day][stop_name]:
                            #  arrival_time = 0
                            print(b.name, route, day, stop_name, arrival_time)
                            time_data_source.append((stop_name, bus_row, arrival_time, route, day))
            TimetableDB.insert_many(time_data_source, fields=[
                TimetableDB.stop_name,
                TimetableDB.bus,
                TimetableDB.arrival_time,
                TimetableDB.route,
                TimetableDB.days]).execute()

            StopsDB.insert_many(stop_data_source, fields=[
                StopsDB.stop_name,
                StopsDB.route,
                StopsDB.bus
            ]).execute()


class BusesDB(Model):
    name = CharField()
    bus_class = Bus(name)

    class Meta:
        database = DB


class TimetableDB(Model):
    stop_name = CharField()
    route = CharField()
    days = CharField()
    bus = ForeignKeyField(BusesDB, related_name="bus")
    arrival_time = TimeField()

    class Meta:
        database = DB


class StopsDB(Model):
    stop_name = CharField()
    route = CharField()
    bus = ForeignKeyField(BusesDB, related_name="bus")
    stop_id = IntegerField(null=True)

    class Meta:
        database = DB

