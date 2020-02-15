import threading
import time
from datetime import datetime

from constants import STOP_FIELDS
from database import Schedule, QueryRecord, Filter, create_database
from functions import convert, time_to_seconds
from functions import get_nearest_actual_schedules
from parsers import Tags
from request import GetStopInfoApiRequest

MAX_QUERY_ITERATIONS = float('inf')

DEFAULT_TIMEOUT = 30
MIN_TIMEOUT = 10


def get_data_from_request(stop_id, _filter):
    stop_request = GetStopInfoApiRequest(stop_id)
    stop_request.run()

    data = stop_request.obtained_data

    return data


class RemoteQueryPerformer:
    def __init__(self, stop_id, route_name):
        self.timeout = DEFAULT_TIMEOUT
        self.iterations_passed = 0

        self.main_thread = threading.Thread(target=self.main, args=[stop_id, route_name, Filter(0, 0)])
        self.main_thread.start()

    def main(self, stop_id, route_name, _filter):
        while self.iterations_passed < MAX_QUERY_ITERATIONS:
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

                # self.timeout = DEFAULT_TIMEOUT
                now = datetime.time(datetime.now())
                now_secs = time_to_seconds(now)

                ya_secs = time_to_seconds(yandex_values[0])

                self.timeout = max(MIN_TIMEOUT, (ya_secs - now_secs) // 2)

                QueryRecord.create(request_time=datetime.now(), bus_income=yandex_values[0],
                                   left_db_border=borders_values[0],
                                   right_db_border=borders_values[1])
            except Exception as e:
                print("No Yandex values", e)
                self.timeout += DEFAULT_TIMEOUT
                QueryRecord.create(request_time=datetime.now())

            self.iterations_passed += 1
            print(self.iterations_passed, 'Requests passed, timeout:', self.timeout)
            time.sleep(self.timeout)


def main():
    create_database(['732'], fill_schedule_flag=True)
    RemoteQueryPerformer(STOP_FIELDS[0]['stop_id'], '732')


if __name__ == '__main__':
    main()
