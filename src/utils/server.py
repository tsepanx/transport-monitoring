import threading
import time
from datetime import datetime

from src.constants import STOP_FIELDS, SERVER_MAX_QUERY_ITERATIONS, SERVER_DEFAULT_TIMEOUT, SERVER_MIN_TIMEOUT
from src.database.filter import Filter
from src.database.functions import create_database
from src.database.models import Schedule, Request
from src.utils.functions import convert
from src.utils.parsers import Tags
from src.utils.request import GetStopInfoApiRequest
from src.utils.time import time_to_seconds


def get_nearest_actual_schedules(expected_values, actual_value):
    int_values = []

    actual_value = actual_value.hour * 60 + actual_value.minute

    for i in range(1, len(expected_values)):
        if expected_values[i] < expected_values[i - 1]:
            day_change = i
            break
    else:
        raise Exception

    i = len(expected_values) - 1
    while i >= day_change:
        int_values.append(expected_values[i].hour * 60 + expected_values[i].minute + 60 * 24)
        i -= 1

    while i >= 0:
        int_values.append(expected_values[i].hour * 60 + expected_values[i].minute)
        i -= 1

    int_values.reverse()

    if actual_value < int_values[0]:
        actual_value += 24 * 60

    if int_values[-1] <= actual_value <= int_values[0]:
        return int_values[-1], int_values[0]

    nearest_lower = binary_search_left(actual_value, int_values)
    nearest_greater = nearest_lower + 1

    return nearest_lower, nearest_greater


def get_data_from_request(stop_id, _filter):
    stop_request = GetStopInfoApiRequest(stop_id)
    stop_request.run()

    data = stop_request.obtained_data

    return data


class RemoteQueryPerformer:
    def __init__(self, stop_id, route_name):
        self.timeout = SERVER_DEFAULT_TIMEOUT
        self.iterations_passed = 0

        self.main_thread = threading.Thread(target=self.main, args=[stop_id, route_name, Filter(0, 0)])
        self.main_thread.start()

    def main(self, stop_id, route_name, _filter):
        while self.iterations_passed < SERVER_MAX_QUERY_ITERATIONS:
            try:
                data = get_data_from_request(stop_id, _filter)
                stop_name_ya = data[Tags.STOP_NAME]

                print(convert(data))
                print(stop_name_ya)
                yandex_values = data[route_name][Tags.ESTIMATED]

                database_values = list(map(lambda x: x.time,
                                           Schedule.by_attribute(route_name, stop_name=stop_name_ya, _filter=_filter)))

                borders = get_nearest_actual_schedules(database_values, yandex_values[0])
                borders_values = database_values[borders[0]], database_values[borders[1]]

                print(*yandex_values, borders_values)

                # self.timeout = SERVER_DEFAULT_TIMEOUT
                now = datetime.time(datetime.now())
                now_secs = time_to_seconds(now)

                ya_secs = time_to_seconds(yandex_values[0])

                self.timeout = max(SERVER_MIN_TIMEOUT, (ya_secs - now_secs) // 2)

                Request.create(time=datetime.now(),
                               bus_income=yandex_values[0],
                               # stop_id=peewee.f,
                               schedule_left=borders_values[0],
                               schedule_right=borders_values[1],
                               timeout=self.timeout)
            except Exception as e:
                print("No Yandex values", e)
                self.timeout += SERVER_DEFAULT_TIMEOUT
                Request.create(time=datetime.now(), timeout=self.timeout)

            self.iterations_passed += 1
            print(self.iterations_passed, 'Requests passed, timeout:', self.timeout)
            time.sleep(self.timeout)


def main():
    create_database(['732'], fill_schedule_flag=True)
    RemoteQueryPerformer(STOP_FIELDS[0]['stop_id'], '732')


if __name__ == '__main__':
    main()


def binary_search_left(x, arr):
    l = -1
    r = len(arr)
    while r - l > 1:
        m = (l + r) // 2
        if arr[m] <= x:
            l = m
        else:
            r = m
    return l