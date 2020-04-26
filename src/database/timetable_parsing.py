import datetime

import requests
from bs4 import BeautifulSoup

from src.database.filter import Filter
from src.database.models import RouteData, Stop, Schedule


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
                stop_row = Stop.create(name_mgt=name_mgt,
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
