import functions as f
import requests
import json
from peewee import *
from bs4 import BeautifulSoup

WORKDAYS = "1111100"
WEEKENDS = "0000011"
ROUTE_AB = "AB"
ROUTE_BA = "BA"


class File:

    def __init__(self, filename, _type="w+"):
        self.full_name = f.FILENAMES_PREFIX + filename
        self.__file_object = open(self.full_name, _type)

    def write(self, data):
        self.file_object.write(data)

    def write_json(self, data):
        self.file_object.write(json.dumps(data, indent=4, separators=(',', ': ')))

    def write_csv(self, array_pos):
        for i in range(len(array_pos)):
            self.write(";".join(map(str, [array_pos[i][1], array_pos[i][0], i + 1, i + 1])))
            self.write("\n")

    def read(self):
        return self.file_object.read()

    def read_json(self):
        return json.loads(self.file_object.read())


class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, b):
        return ((b.x - self.x) ** 2 + (b.y - self.y) ** 2) ** 0.5


class Bus:
    paths_list = []
    timetable = {
        ROUTE_AB:
            {WORKDAYS: [], WEEKENDS: []},
        ROUTE_BA:
            {WORKDAYS: [], WEEKENDS: []}
    }

    def __init__(self, name="0"):
        self.name = name

    def get_path(self, route=ROUTE_AB, days=WORKDAYS):
        for i in self.paths_list:
            if i.route == route and i.days == days:
                return i

    def get_timetable(self, route=ROUTE_AB, days=WORKDAYS, stop_filter="all"):

        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.name}&date={days}&direction={route}&waypoint={stop_filter}"

        request = requests.get(url_string)
        soup = BeautifulSoup(''.join(request.text), features="html.parser")

        stop_names = soup.findAll('h2')[:-1]

        for i in range(len(stop_names)): stop_names[i] = stop_names[i].text
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

                    output.append(f.datetime.time(hours, minutes))

            res_dict[stop_names[i - 1]] = output

        self.timetable[route][days] = res_dict

    def get_stops(self, route=ROUTE_AB, days=WORKDAYS):
        url_string = f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={self.name}&date={days}&direction={route}'
        raw_stops_list = requests.get(url_string)
        stops_list = []
        for stop in raw_stops_list.text.split('\n'):
            if stop != "":
                stops_list.append(stop)

        p = Path(self.name, route, days, stops_list)
        return p

    def get_all_stops(self, routes=(ROUTE_AB, ROUTE_BA), days=(WORKDAYS, WEEKENDS)):
        try:
            res = []
            for day in days:
                for route in routes:
                    p = self.get_stops(route, day)
                    res.append(p)
            self.paths_list = res[:]
        except Exception:
            raise Exception("No internet connection")

    def get_all_timetable(self, routes=(ROUTE_AB, ROUTE_BA), days=(WORKDAYS, WEEKENDS)):
        for route in routes:
            for day in days:
                self.timetable[route][day] = self.get_timetable(route, day)


class Path:
    name = ""
    route = 0
    days = 0
    stops = []

    def __init__(self, name, route=ROUTE_AB, days=WORKDAYS, path=()):
        self.name = name
        self.route = route
        self.days = days
        self.stops = path

    def __eq__(self, b):
        return self.stops == b.stops


class BusesDB(Model):
    name = CharField()
    bus_class = Bus(name)

    class Meta:
        database = f.db


class Time(Model):
    stop_name = CharField()
    route = CharField()
    days = CharField()
    bus = ForeignKeyField(BusesDB, related_name="bus")
    arrival_time = TimeField()

    class Meta:
        database = f.db
