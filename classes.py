import json
import time
import threading

import requests
from bs4 import BeautifulSoup
from yandex_transport_webdriver_api import YandexTransportProxy

from functions import *


class File:

    def __init__(self, filename, extension):
        self.full_name = get_full_filename(filename, extension)
        self.__extension = extension
        is_already_created = os.path.exists(self.full_name)

        self.__open("r" if is_already_created else "w+")
        print(self.full_name, self.__extension)

    def __open(self, _type):
        self.__file_object = open(self.full_name, _type)

    def raw_write(self, data):
        self.__open("w+")
        self.__file_object.write(data)

    def raw_read(self):
        self.__open("r")
        return self.__file_object.read()


class JsonFile(File):

    def __init__(self, _bus_name, _request_type):
        self.data_dict = None
        self.request_type = _request_type  # Request.GET_STOP_INFO if _stop_id else Request.GET_LINE
        self.data_dict = dict()

        super().__init__(self.request_type.value + _bus_name, "json")

    def write(self, data):
        d = json.dumps(data, indent=4, separators=(',', ': '))
        self.raw_write(d)

    def read(self):
        return json.loads(self.raw_read())

    def get_all_points_recursively(self):
        return recursive_descent(self.raw_read())


class GetStopInfoJsonFile(JsonFile):
    def __init__(self, bus_name, stop_id):
        super().__init__(bus_name, Request.GET_STOP_INFO)

        self.bus_name = bus_name
        self.stop_id = stop_id

    def execute(self, proxy):
        data = proxy.get_stop_info(get_stop_url(self.stop_id))
        self.write(data)

        self.data_dict = self.__get_transport_schedules()
        return self

    def __get_transport_schedules(self):
        data = self.read()

        res_dict = dict()

        props = data["data"]["properties"]
        stop_russian_fullname = props["name"]
        transport_data = props["StopMetaData"]["Transport"]

        res_dict[Tags.STOP_NAME] = stop_russian_fullname

        for bus in transport_data:
            if bus["type"] != "bus":
                continue

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


class GetLineJsonFile(JsonFile):
    def __init__(self, _line_id, _thread_id, _bus_name):
        self.line_id = _line_id
        self.thread_id = _thread_id

        super().__init__(_bus_name, Request.GET_LINE)

    def execute(self, proxy):
        data = proxy.get_line(get_line_url(self.line_id, self.thread_id))
        self.write(data)

        self.data_dict = self.__get_line_data()
        return self

    def __get_line_data(self):
        data = self.read()

        res_dict = {}

        stops_list = data["data"]["features"][0]["features"]

        for stop in stops_list:
            if Tags.PROPERTIES not in stop:
                continue

            properties = stop[Tags.PROPERTIES][Tags.STOP_META_DATA]
            name = properties["name"]
            raw_id = properties["id"]

            if "stop__" in raw_id:
                raw_id = int(raw_id[6:])
            else:
                raw_id = int(raw_id)

            res_dict[raw_id] = name

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

    def get_timetable(self, route=TimetableFilter.ROUTE_AB, days=TimetableFilter.WORKDAYS, stop_filter="all"):

        url_string = f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={self.name}&date={days}&direction={route}&waypoint={stop_filter}"
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

        self.timetable[route][days] = res_dict
        return self.timetable[route][days]

    def get_all_timetable(self, routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA),
                          days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS)):
        for route in routes:
            for day in days:
                self.get_timetable(route=route, days=day)

    @staticmethod
    def get_buses_list():
        r = requests.get('http://www.mosgortrans.org/pass3/request.ajax.php?list=ways&type=avto')
        directions = ['AB', 'BA']
        for i in r.text.split():
            days = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=days&type=avto&way={i}')
            for day in days.text.split():
                for direction in directions:
                    stops = requests.get(
                        f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={i}&date={day}&direction={direction}')
                    stops_list = []
                    for stop in stops.text.split('\n'):
                        if stop == '':
                            break
                        else:
                            stops_list.append(stop)
            return stops_list


class Database:

    def __init__(self, _list, db=GLOBAL_DB, _filter_routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA),
                 _filter_days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS)):
        self.db = db

        self.buses_list = _list
        self.filter_routes = _filter_routes
        self.filter_days = _filter_days

    def create(self):
        if not os.path.exists(PROJECT_PREFIX + MAIN_DB_FILENAME):
            self.__fill_database(filter_routes=self.filter_routes, filter_days=self.filter_days)
        else:
            print("=== database already exists! ===")
        return self

    @staticmethod
    def get_filtered_rows_from_db(bus, stop_name, _route=TimetableFilter.ROUTE_AB, _days=TimetableFilter.WORKDAYS):
        res = []
        query = TimetableDB.select().where(
            TimetableDB.route == _route,
            TimetableDB.days == _days,
        ).order_by(TimetableDB.stop_name)

        for row in query:
            if are_equals(row.stop_name, stop_name):
                if row.bus.name == bus:
                    res.append(row.arrival_time)

        return res

    def __fill_database(self, filter_routes=(TimetableFilter.ROUTE_AB, TimetableFilter.ROUTE_BA),
                        filter_days=(TimetableFilter.WORKDAYS, TimetableFilter.WEEKENDS), visual=False):
        self.db.create_tables(DATABASE_TIMETABLES_LIST)

        for bus_name in self.buses_list:
            time_data_source = []
            stop_data_source = []

            bus = Bus(bus_name)
            bus.get_all_timetable(routes=filter_routes, days=filter_days)

            bus_row = BusesDB.create(name=bus.name)
            print(bus.name)

            for route in bus.timetable:
                for day in bus.timetable[route]:
                    for stop_name in bus.timetable[route][day]:
                        stop_data_source.append(
                            (stop_name,
                             route,
                             bus_row))

                        for arrival_time in bus.timetable[route][day][stop_name]:
                            time_data_source.append((stop_name, bus_row, arrival_time, route, day))
                            if visual:
                                print(bus.name, route, day, stop_name, arrival_time)
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


class ServerManager:
    def __init__(self, bus_name, stop_id, proxy, interval=30, iterations=2):
        self.interval = interval
        self.made_iterations = 0
        # self.execute(iterations, bus_name, stop_id, proxy)

        self.main_thread = threading.Thread(target=self.execute,
                                            args=[iterations, bus_name, stop_id, proxy])
        self.main_thread.start()

    def execute(self, count, bus_name, stop_id, proxy):
        while self.made_iterations < count:
            thread = threading.Thread(target=self.main_func,
                                      args=[bus_name, stop_id, proxy])
            thread.start()
            self.made_iterations += 1
            time.sleep(self.interval)

    @staticmethod
    def main_func(bus_name, stop_id, proxy):
        current_route = TimetableFilter.ROUTE_AB
        current_day = TimetableFilter.WORKDAYS if is_today_workday() else TimetableFilter.WEEKENDS

        stop_file = GetStopInfoJsonFile(bus_name, stop_id).execute(proxy)

        stop_name = stop_file.data_dict[Tags.STOP_NAME]

        estimated_list = stop_file.data_dict[bus_name][Tags.ESTIMATED]
        scheduled_list = stop_file.data_dict[bus_name][Tags.SCHEDULED]

        if len(estimated_list + scheduled_list) == 0:
            print("--- No buses on path now ---")
            return

        api_times = (estimated_list + scheduled_list)
        db_times = Database.get_filtered_rows_from_db(bus_name, stop_name, current_route, current_day)

        nearest_times = calculate_time_values_difference(api_times, db_times)

        print(api_times[0], *nearest_times, sep="\n")
        print("=====")


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
