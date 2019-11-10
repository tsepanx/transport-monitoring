import requests
from datetime import *
from bs4 import BeautifulSoup
from peewee import *

db = SqliteDatabase('db.db')

WORKDAYS = "1111100"
WEEKENDS = "0000011"
ROUTE_AB = "AB"
ROUTE_BA = "BA"

class DB_Bus(Model):
    name = CharField()

    class Meta:
        database = db

class Time(Model):
    stop_name = CharField()
    bus = ForeignKeyField(DB_Bus, related_name="bus")
    time = TimeField()
    

    class Meta:
        database = db

class Bus:
    paths_list = []

    def __init__(self, name="0"):
        self.name = name
        self.get_all_stops()

    def get_path(self, route=ROUTE_AB, days=WORKDAYS):
        for i in self.paths_list:
            if i.route == route and i.days == days:
                return i

    def get_bus_timetable(self, stop_filter="all", route=ROUTE_AB, days=WORKDAYS):

        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.number}&date={days}&direction={route}&waypoint={stop_filter}"

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

                    output.append(time(hours, minutes))

            res_dict[stop_names[i - 1]] = output

        return res_dict

    def get_stops(self, route=ROUTE_AB, day=WORKDAYS):
        url_string = f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={self.number}&date={day}&direction={route}'
        raw_stops_list = requests.get(url_string)
        stops_list = []
        for stop in raw_stops_list.text.split('\n'):
            if stop != "":
                stops_list.append(stop)

        p = Path(self.number, route, day, stops_list)
        return p

    def get_all_stops(self, routes=(ROUTE_AB, ROUTE_BA), days=(WORKDAYS, WEEKENDS)):
        res = []
        for day in days:
            for route in routes:
                p = self.get_stops(route, day)
                res.append(p)

        self.paths_list = res[:]

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

def init_database():
    db.connect()
    db.create_tables([DB_Bus, Time])

    bus1 = DB_Bus.create(id=1, name="101")
    bus2 = DB_Bus.create(id=300, name="200")

    time1 = Time.create(id=1, stop_name="lol", bus=bus2, time=time(hour=5, minute=36))

init_database()