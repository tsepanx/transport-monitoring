import threading
import time
from datetime import timedelta, datetime

from constants import Tags, Filter
from functions import get_nearest_actual_schedules

from database import ArrivalTime, ServerTimeFix
from request import YandexApiRequest, Request


class ServerManager:
    def __init__(self, route_name,
                 interval,
                 duration=timedelta(seconds=60)):
        self.interval = interval
        self.made_iterations = 0

        iterations = round(duration.seconds / interval)
        self.main_thread = threading.Thread(target=self.run_async,
                                            args=[iterations], kwargs={'route_name': route_name,
                                                                       'filter': Filter(0, 0)})
        self.main_thread.start()

    def run_async(self, count, **kwargs):
        while self.made_iterations < count:
            value = do_request(**kwargs)
            ServerTimeFix.create(request_time=datetime.now(), estimated_time=value)

            self.made_iterations += 1
            print(self.made_iterations)
            time.sleep(self.interval)


def do_request(route_name, filter=Filter(0, 0)):
    stop_request = YandexApiRequest(Request.GET_STOP_INFO, route_name)
    stop_request.run()

    data = stop_request.obtained_data

    stop_name_ya = data[Tags.STOP_NAME]

    yandex_values = data[route_name][Tags.ESTIMATED]

    database_values = list(map(lambda x: x.arrival_time, ArrivalTime.by_stop_name(route_name, stop_name_ya, filter)))

    if not yandex_values:
        print("No Yandex values")

    nearest_schedules = get_nearest_actual_schedules(database_values, yandex_values[0])

    print(nearest_schedules)

    return yandex_values[0]
