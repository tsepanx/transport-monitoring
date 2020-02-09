import threading
import time
from datetime import datetime

from parsers import Tags
from database import Schedule, QueryRecord, Filter
from functions import get_nearest_actual_schedules
from request import GetStopInfoApiRequest

MAX_QUERY_ITERATIONS = 100


def do_request(route_name, _filter):
    stop_request = GetStopInfoApiRequest(route_name)
    stop_request.run()

    data = stop_request.obtained_data

    return data


class RemoteQueryPerformer:
    def __init__(self, route_name, interval):
        self.interval = interval
        self.iterations_passed = 0

        self.main_thread = threading.Thread(target=self.main, args=[route_name, Filter(0, 0)])
        self.main_thread.start()

    def main(self, route_name, _filter):
        while self.iterations_passed < MAX_QUERY_ITERATIONS:
            data = do_request(route_name, _filter)

            stop_name_ya = data[Tags.STOP_NAME]
            yandex_values = data[route_name][Tags.ESTIMATED]

            if not yandex_values:
                print("No Yandex values")
                QueryRecord.create(request_time=datetime.now(),
                                   estimated_time=None)

            else:
                database_values = list(map(lambda x: x.arrival_time,
                                           Schedule.by_attribute(route_name, attr_value=stop_name_ya, _filter=_filter)))

                borders = get_nearest_actual_schedules(database_values, yandex_values[0])

                QueryRecord.create(request_time=datetime.now(),
                                   estimated_time=yandex_values[0],
                                   left_db_border=borders[0],
                                   right_db_border=borders[1])

            self.iterations_passed += 1
            print(self.iterations_passed)
            time.sleep(self.interval)
