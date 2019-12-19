import threading
import time

import deprecation
import requests
from bs4 import BeautifulSoup
from yandex_transport_webdriver_api import YandexTransportProxy
from File import GetStopInfoJsonFile

from constants import *
from functions import *


class TimetableParser:
    paths_list = []
    timetable = {
        TimetableFilter.WAYS[0]:
            {TimetableFilter.DAYS[0]: {}, TimetableFilter.DAYS[1]: {}},
        TimetableFilter.WAYS[1]:
            {TimetableFilter.DAYS[0]: {}, TimetableFilter.DAYS[1]: {}}
    }

    def __init__(self, route_name):
        self.route_name = route_name

    def __get_timetable(self, way=TimetableFilter.WAYS[0], days=TimetableFilter.DAYS[0], stop_filter="all"):

        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.route_name}&date={days}&direction={way}&waypoint={stop_filter}"
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

        self.timetable[way][days] = res_dict
        return self.timetable[way][days]

    def get_all_timetable(self, ways=TimetableFilter.WAYS,
                          days=TimetableFilter.DAYS):
        for way in ways:
            for day in days:
                self.__get_timetable(way=way, days=day)

    @staticmethod
    @deprecation.deprecated("Dont use it")
    def get_buses_list():
        stops_list = []
        r = requests.get('http://www.mosgortrans.org/pass3/request.ajax.php?list=ways&type=avto')
        for i in r.text.split():
            days = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=days&type=avto&way={i}')
            for day in days.text.split():
                for way in TimetableFilter.WAYS:
                    stops = requests.get(
                        f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&'
                        f'way={i}&'
                        f'date={day}&'
                        f'direction={way}')
                    for stop in stops.text.split('\n'):
                        if stop == '':
                            break
                        else:
                            stops_list.append(stop)
            return stops_list


class Database:

    def __init__(self, routes_list, db=GLOBAL_DB,
                 filter_ways=TimetableFilter.WAYS,
                 filter_days=TimetableFilter.DAYS):
        self.db = db

        self.routes_list = routes_list
        self.filter_ways = filter_ways
        self.filter_days = filter_days

    def create(self):
        if not os.path.exists(PROJECT_PREFIX + MAIN_DB_FILENAME):
            self.__fill_database(filter_ways=self.filter_ways, filter_days=self.filter_days)
        else:
            print("=== database already exists! ===")
        return self

    def __fill_database(self,
                        filter_ways=TimetableFilter.WAYS,
                        filter_days=TimetableFilter.WAYS):
        self.db.create_tables(DATABASE_TIMETABLES_LIST)

        for route_name in self.routes_list:
            time_data_source = []
            stop_data_source = []

            parser = TimetableParser(route_name)
            parser.get_all_timetable(filter_ways, filter_days)

            route_row = RouteData.create(name=parser.route_name)
            print(parser.route_name)

            for route in parser.timetable:
                for day in parser.timetable[route]:
                    for stop_name in parser.timetable[route][day]:
                        stop_data_source.append(
                            (stop_name,
                             route,
                             route_row))

                        for arrival_time in parser.timetable[route][day][stop_name]:
                            time_data_source.append((stop_name, route_row, arrival_time, route, day))
                            # print(parser.route_name, route, day, stop_name, arrival_time)
            ArrivalTime.insert_many(time_data_source, fields=[
                ArrivalTime.stop_name,
                ArrivalTime.route_name,
                ArrivalTime.arrival_time,
                ArrivalTime.way,
                ArrivalTime.days]).execute()

            StopData.insert_many(stop_data_source, fields=[
                StopData.stop_name,
                StopData.way,
                StopData.route_name
            ]).execute()

    @staticmethod
    def get_filtered_rows_from_db(route_name, stop_name, way=TimetableFilter.WAYS[0], days=TimetableFilter.DAYS[0]):
        res = []
        query = ArrivalTime.select().where(
            ArrivalTime.way == way,
            ArrivalTime.days == days,
        ).order_by(ArrivalTime.stop_name)

        for row in query:
            if are_equals(row.stop_name, stop_name):
                if row.route_name.name == route_name:
                    res.append(row.arrival_time)

        return res


class ServerManager:
    def __init__(self, route_name, stop_id, proxy,
                 interval,
                 iterations=None,
                 delta_time=datetime.timedelta(seconds=60)):

        if not iterations:
            iterations = round(delta_time.seconds / interval)

        self.interval = interval
        self.made_iterations = 0
        print(iterations)

        self.main_thread = threading.Thread(target=self.execute,
                                            args=[iterations, route_name, stop_id, proxy])
        self.main_thread.start()

    def execute(self, count, route_name, stop_id, proxy):
        while self.made_iterations < count:
            thread = threading.Thread(target=self.write_to_db,
                                      args=[route_name, stop_id, proxy])
            thread.start()
            self.made_iterations += 1
            time.sleep(self.interval)

    def write_to_db(self, route_name, stop_id, proxy):
        value = self.main_func(route_name, stop_id, proxy)

        ServerTimeFix.create(request_time=datetime.datetime.now(), estimated_time=value)

    def main_func(self, route_name, stop_id, proxy):
        current_route = TimetableFilter.WAYS[0]
        current_day = TimetableFilter.DAYS[is_today_workday()]

        stop_file = GetStopInfoJsonFile(route_name, stop_id).execute(proxy)

        stop_name = stop_file.data_dict[Tags.STOP_NAME]

        estimated_list = stop_file.data_dict[route_name][Tags.ESTIMATED]
        scheduled_list = stop_file.data_dict[route_name][Tags.SCHEDULED]

        if len(estimated_list + scheduled_list) == 0:
            print("--- No buses on path now ---")
            return None

        api_times = (estimated_list + scheduled_list)
        db_times = Database.get_filtered_rows_from_db(route_name, stop_name, current_route, current_day)

        try:
            nearest_times = calculate_time_values_difference(api_times, db_times)
        except Exception:
            return None
        res_time = api_times[0]

        print("real time:", res_time, "times from db:", *nearest_times, sep="\n")
        print(self.made_iterations, "request finished")
        print("=====\n")

        return res_time


class MyYandexTransportProxy(YandexTransportProxy):

    def __init__(self, host, port):
        super().__init__(host, port)

    def get_all_info(self, url, query_id=None, blocking=True, timeout=0, callback=None):
        print("GetAllInfo")
        # super()._execute_get_query("getLine", url, query_id, blocking, timeout, callback)
        return super().get_all_info(url, query_id, blocking, timeout, callback)

    def get_stop_info(self, url, query_id=None, blocking=True, timeout=0, callback=None):
        print("GetStopInfo")
        return super().get_stop_info(url, query_id, blocking, timeout, callback)

    def get_line(self, url, query_id=None, blocking=True, timeout=0, callback=None):
        print("GetLine")
        return super().get_line(url, query_id, blocking, timeout, callback)
