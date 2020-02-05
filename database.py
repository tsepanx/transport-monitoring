import time
from datetime import time

import os

import requests
from bs4 import BeautifulSoup
from peewee import *

from constants import MY_DATABASE, DATABASE_PATH
from functions import lewen_length, convert


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


class RouteData(BaseModel):
    name = CharField()


class Schedule(BaseModel):
    stop_name = CharField()
    way = CharField()
    days = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    arrival_time = TimeField()

    @staticmethod
    def by_stop_name(route_name, stop_name, _filter=Filter()):
        way = _filter.way_filter
        days = _filter.week_filter

        res = []
        query = Schedule.select().where(
            (Schedule.way << way) &
            (Schedule.days << days)
        ).order_by(Schedule.stop_name)

        for row in query:
            if lewen_length(row.stop_name, stop_name) <= 5:
                if row.route_name.name == route_name:
                    res.append(row)

        return res

    def by_stop_id(self, route_name, stop_id, _filter=Filter()):
        stop_name = StopData.by_id(stop_id)
        self.by_stop_name(route_name, stop_name, _filter)


class StopData(BaseModel):
    stop_name = CharField()
    way = CharField()
    route_name = ForeignKeyField(RouteData, related_name="bus")
    stop_id = IntegerField(null=True)

    @staticmethod
    def by_id(stop_id):
        return None  # TODO implement it


class QueriesRecords(BaseModel):
    request_time = TimeField()
    estimated_time = TimeField()


DATABASE_TIMETABLES_LIST = [RouteData, Schedule, StopData, RemoteQueriesRecords]


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

                    output.append(time(hours, minutes))

            res_dict[stop_names[i - 1]] = output

        self.obtained_timetable[Filter(way_filter=way, week_filter=days)] = res_dict

    def obtain_all_timetables(self):
        _filter = Filter()

        for way in _filter.way_filter:
            for day in _filter.week_filter:
                self.__obtain_parsed_timetable(days=day, way=way)


def obtain_routes_sources(routes_list):
    res = {}

    for route_name in routes_list:
        res[route_name] = {}
        arrival_times_source = []
        stop_data_source = []

        parser = TimetableParser(route_name)
        parser.obtain_all_timetables()

        route_row = RouteData.create(name=parser.route_name)
        print(parser.route_name)

        for routes_filter in parser.obtained_timetable:
            for stop_name in parser.obtained_timetable[routes_filter]:
                stop_data_source.append(
                    (stop_name,
                     routes_filter.way_filter[0],
                     route_row))
                for arrival_time in parser.obtained_timetable[routes_filter][stop_name]:
                    new_source_row = (stop_name,
                                      route_row,
                                      arrival_time,
                                      routes_filter.way_filter[0],
                                      routes_filter.week_filter[0])

                    arrival_times_source.append(new_source_row)
        res[route_name][Schedule] = arrival_times_source
        res[route_name][StopData] = stop_data_source

    return res


def insert_many(sources):
    for route_name in sources:
        Schedule.insert_many(sources[route_name][Schedule], fields=[
            Schedule.stop_name,
            Schedule.route_name,
            Schedule.arrival_time,
            Schedule.way,
            Schedule.days]).execute()

        StopData.insert_many(sources[route_name][StopData], fields=[
            StopData.stop_name,
            StopData.way,
            StopData.route_name
        ]).execute()


def create_database(routes_list, db=MY_DATABASE):
    if not os.path.exists(DATABASE_PATH):
        db.create_tables(DATABASE_TIMETABLES_LIST)
        sources = obtain_routes_sources(routes_list)
        insert_many(sources)
    else:
        print("=== database already exists! ===")
