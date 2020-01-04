import threading
import time
from datetime import timedelta, datetime

from classes import get_filtered_rows_from_db
from constants import *
from file import GetStopInfoJsonFile
from parsers import parse_get_stop_info_json


class ServerManager:
    def __init__(self, route_name, stop_id, proxy,
                 interval,
                 iterations=None,
                 delta_time=timedelta(seconds=60)):

        if not iterations:
            iterations = round(delta_time.seconds / interval)

        self.interval = interval
        self.made_iterations = 0

        self.main_thread = threading.Thread(target=self.run_async,
                                            args=[iterations], kwargs={'route_name': route_name,
                                                                       'stop_id': stop_id,
                                                                       'proxy': proxy,
                                                                       'filter': Filter(0, 0)
                                                                       })
        self.main_thread.start()

    def run_async(self, count, **kwargs):
        while self.made_iterations < count:
            value = self.main(kwargs)
            ServerTimeFix.create(request_time=datetime.now(), estimated_time=value)

            self.made_iterations += 1
            time.sleep(self.interval)

    def main(self, route_name=None, stop_id=None, proxy=None, filter=None):
        stop_file = GetStopInfoJsonFile(route_name, proxy, stop_id).write_to_file()
        data = parse_get_stop_info_json(stop_file.data_dict)
        stop_name = data[Tags.STOP_NAME]

        estimated_list = data[route_name][Tags.ESTIMATED]
        db_times = get_filtered_rows_from_db(route_name, stop_name, filter)

        if len(estimated_list) == 0:
            print("--- No buses on path now ---")
            return None

        nearest_income = estimated_list[0]

        close_values = {}
        for i, t in enumerate(db_times):
            if t >= nearest_income:
                close_values = [db_times[i - 1], t]
                break

        print("real time:", nearest_income, "times from db:", *close_values, sep="\n")
        print(self.made_iterations, "request finished")
        print("=====\n")

        return nearest_income


def main():
    current_route_name = "732"
    current_stop_id = ROUTES_FIELDS[current_route_name]['stop_id']

    duration = int(input("duration: "))
    interval = int(input("interval: "))

    manager = ServerManager(current_route_name, current_stop_id, proxy, interval=interval,
                            delta_time=timedelta(hours=duration))

    while manager.main_thread.is_alive():
        pass


if __name__ == '__main__':
    main()
