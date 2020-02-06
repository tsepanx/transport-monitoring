import threading
import time
from datetime import datetime

from parsers import Tags
from database import Schedule, QueryRecord, Filter
from functions import get_nearest_actual_schedules
from request import GetStopInfoApiRequest

MAX_QUERY_ITERATIONS = 100


class RemoteQueryPerformer:
    def __init__(self, route_name, interval):
        self.interval = interval
        self.iterations_passed = 0

        self.main_thread = threading.Thread(target=self.run_async,
                                            kwargs={'route_name': route_name, '_filter': Filter(0, 0)})
        self.main_thread.start()

    def run_async(self, **kwargs):
        while self.iterations_passed < MAX_QUERY_ITERATIONS:
            value = do_request(**kwargs)
            QueryRecord.create(request_time=datetime.now(), estimated_time=value)

            self.iterations_passed += 1
            print(self.iterations_passed)
            time.sleep(self.interval)


def do_request(route_name, _filter):
    stop_request = GetStopInfoApiRequest(route_name)
    stop_request.run()

    data = stop_request.obtained_data

    stop_name_ya = data[Tags.STOP_NAME]

    yandex_values = data[route_name][Tags.ESTIMATED]

    database_values = list(map(lambda x: x.arrival_time,
                               Schedule.by_stop_name(route_name, stop_name_ya, _filter)))

    if not yandex_values:
        print("No Yandex values")

    nearest_schedules = get_nearest_actual_schedules(database_values, yandex_values[0])

    print(nearest_schedules)

    return yandex_values[0]
