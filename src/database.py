import datetime

import requests
from bs4 import BeautifulSoup
from peewee import *

from src.constants import MY_DATABASE, DATABASE_PATH, does_exist, determine_same_stop_names
from src.functions import convert


class Filter:
    def __init__(self, way_filter=None, week_filter=None):
        self.ways = ("AB", "BA")
        self.days = ("1111100", "0000011")

        if isinstance(way_filter, str):
            self.way_filter = [way_filter]
        else:
            self.way_filter = self.ways if way_filter is None else [self.ways[way_filter]]

        if isinstance(week_filter, str):
            self.week_filter = [week_filter]
        else:
            self.week_filter = self.days if week_filter is None else [self.days[week_filter]]


class BaseModel(Model):
    class Meta:
        database = MY_DATABASE

    def __str__(self):
        return convert(vars(self)['__data__'])

    def __iter__(self):
        simple_attrs = vars(self)['__data__']
        rel_attrs = vars(self)['__rel__']

        for rel in rel_attrs:
            for simple_rel_attr in rel_attrs[rel]:
                yield simple_rel_attr

        for attr in simple_attrs:
            if attr not in ['id']:
                yield attr, simple_attrs[attr]


class RouteData(BaseModel):  # Buses
    name = CharField()


class YandexStop(BaseModel):
    name_ya = TextField()
    id_ya = IntegerField()


class StopData(BaseModel):
    name_mgt = CharField()
    route = ForeignKeyField(RouteData, related_name='bus', backref='stop')
    direction = CharField()

    ya_stop = ForeignKeyField(YandexStop, null=True, related_name='ya_stop', backref='stop')


class Schedule(BaseModel):
    stop = ForeignKeyField(StopData, related_name='stop', backref='schedule')
    weekdays = CharField()
    time = TimeField()

    @staticmethod
    def by_attribute(route_name, stop_id=None, stop_name=None, _filter=Filter()):
        way = _filter.way_filter
        days = _filter.week_filter

        res = []
        query = Schedule.select().where(Schedule.weekdays << days)

        for row in query:
            if row.stop.direction in way:
                if (stop_id is not None) and stop_id != row.stop.id:
                    continue
                elif (stop_name is not None) and not determine_same_stop_names(stop_name, row.stop.name_mgt):
                    continue

                if row.stop.route.name == route_name:
                    res.append(row)

        return res


class QueryRecord(BaseModel):
    request_time = DateTimeField()
    bus_income = TimeField(null=True)
    left_db_border = TimeField(null=True)
    right_db_border = TimeField(null=True)
    timeout = IntegerField()
    stop_id = ForeignKeyField(StopData, null=True, related_name='stop', backref='queryrecord')


DATABASE_TIMETABLES_LIST = [Schedule, RouteData, StopData, QueryRecord, YandexStop]


class TimetableParser:
    paths_list = []

    def __init__(self, route_name):
        self.route_name = route_name
        self.obtained_timetable = {}

    def __obtain_parsed_timetable(self, days, way):
        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.route_name}&date={days}&direction={way}&waypoint=all"
        print(url_string)

        request = requests.get(url_string)
        soup = BeautifulSoup(''.join(request.text), features="html.parser")

        stop_names = soup.findAll('h2')[:-1]

        for i in range(len(stop_names)):
            stop_names[i] = stop_names[i].text

        res_dict = dict.fromkeys(stop_names, [])

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

        self.obtained_timetable[Filter(way_filter=way, week_filter=days)] = res_dict

    def obtain_all_timetables(self, _filter=Filter()):
        for way in _filter.way_filter:
            for day in _filter.week_filter:
                self.__obtain_parsed_timetable(days=day, way=way)


def gather_schedule_sources(routes_list, _filter=Filter()):
    res = {}

    for route_name in routes_list:
        schedule_source = []

        parser = TimetableParser(route_name)
        parser.obtain_all_timetables(_filter)

        route_row = RouteData.create(name=parser.route_name)
        print(parser.route_name)

        for routes_filter in parser.obtained_timetable:
            for name_mgt in parser.obtained_timetable[routes_filter]:
                stop_row = StopData.create(name_mgt=name_mgt,
                                           route=route_row,
                                           direction=routes_filter.way_filter[0],
                                           stop_id=None)

                for arrival_time in parser.obtained_timetable[routes_filter][name_mgt]:
                    new_source_row = (stop_row, routes_filter.week_filter[0], arrival_time)

                    schedule_source.append(new_source_row)
        res[route_name] = schedule_source

    return res


def fill_schedule(sources):
    for route_name in sources:
        Schedule.insert_many(sources[route_name], fields=[
            Schedule.stop,
            Schedule.weekdays,
            Schedule.time
        ]).execute()


def create_database(routes_list, fill_schedule_flag=False, db=MY_DATABASE, _filter=Filter()):
    if not does_exist(DATABASE_PATH):
        db.create_tables(DATABASE_TIMETABLES_LIST)
    else:
        print("=== database already exists! ===")
        return

    if fill_schedule_flag:
        sources = gather_schedule_sources(routes_list, _filter)
        fill_schedule(sources)
