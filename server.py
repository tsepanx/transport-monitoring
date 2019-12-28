import threading
import time
from datetime import timedelta, datetime

from classes import get_filtered_rows_from_db
from constants import *
from file import GetStopInfoJsonFile
from functions import get_closest_values


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
                                            args=[iterations, route_name, stop_id, proxy, Filters(0, 0)])
        self.main_thread.start()

    def run_async(self, count, route_name, stop_id, proxy, _filter):
        while self.made_iterations < count:
            value = self.main(route_name, stop_id, proxy, _filter)
            ServerTimeFix.create(request_time=datetime.now(), estimated_time=value)

            self.made_iterations += 1
            time.sleep(self.interval)

    def main(self, route_name, stop_id, proxy, _filter):
        stop_file = GetStopInfoJsonFile(route_name, stop_id).execute(proxy)
        stop_name = stop_file.data_dict[Tags.STOP_NAME]

        estimated_list = stop_file.data_dict[route_name][Tags.ESTIMATED]
        scheduled_list = stop_file.data_dict[route_name][Tags.SCHEDULED]

        if len(estimated_list + scheduled_list) == 0:
            print("--- No buses on path now ---")
            return None

        real_values = estimated_list + scheduled_list
        db_times = get_filtered_rows_from_db(route_name, stop_name, _filter)

        res_time = real_values[0]
        close_values = get_closest_values(res_time, db_times)

        print("real time:", res_time, "times from db:", *close_values, sep="\n")
        print(self.made_iterations, "request finished")
        print("=====\n")

        return res_time


def main():
    current_route_name = "732"
    current_stop_id = routes_fields[current_route_name]['main_stop_id']

    duration = int(input("duration: "))
    interval = int(input("interval: "))

    manager = ServerManager(current_route_name, current_stop_id, proxy, interval=interval,
                            delta_time=timedelta(hours=duration))

    while manager.main_thread.is_alive():
        pass


if __name__ == '__main__':
    main()
