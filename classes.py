import requests, json, enum, time
from bs4 import BeautifulSoup
from peewee import *

db = SqliteDatabase('db3.db')

# class Constants(enum.Enum):
WORKDAYS = "1111100"
WEEKENDS = "0000011"
ROUTE_AB = "AB"
ROUTE_BA = "BA"

def init_database(raw_buses_list, filter_routes=(ROUTE_AB, ROUTE_BA), filter_days=(WORKDAYS, WEEKENDS)):
    db.create_tables([BusesDB, Time])
      
    for i in range(first_buses):
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

def get_stop_url(id):
      return "https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__" + str(id)

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
                ROUTE_AB : 
                    {WORKDAYS : [], WEEKENDS : []}, 
                ROUTE_BA : 
                    {WORKDAYS : [], WEEKENDS : []}
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

                    output.append(time(hours, minutes))

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
            raise "No internet connection"
    
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
        database = db

class Time(Model):
    stop_name = CharField()
    route = CharField()
    days = CharField()
    bus = ForeignKeyField(BusesDB, related_name="bus")
    arrival_time = TimeField()
    

    class Meta:
        database = db
