import threading
import time
from datetime import datetime, timedelta

from parsers import Tags
from database import Schedule, QueryRecord, Filter, create_database
from functions import get_nearest_actual_schedules
from request import GetStopInfoApiRequest
from constants import STOP_FIELDS
from functions import convert

MAX_QUERY_ITERATIONS = 100


def do_request(stop_id, _filter):
    stop_request = GetStopInfoApiRequest(stop_id)
    stop_request.run()

    data = stop_request.obtained_data

    print(convert(data))

    return data


class RemoteQueryPerformer:
    def __init__(self, stop_id, route_name, interval):
        self.interval = interval
        self.iterations_passed = 0

        self.main_thread = threading.Thread(target=self.main, args=[stop_id, route_name, Filter(0, 0)])
        self.main_thread.start()

    def main(self, stop_id, route_name, _filter):
        while self.iterations_passed < MAX_QUERY_ITERATIONS:
            data = do_request(stop_id, _filter)

            stop_name_ya = data[Tags.STOP_NAME]
            print(stop_name_ya)
            yandex_values = data[route_name][Tags.ESTIMATED]

            if not yandex_values:
                print("No Yandex values")
                QueryRecord.create(request_time=datetime.now(),
                                   estimated_time=None)

            else:
                database_values = list(map(lambda x: datetime.now() + timedelta(hours=x.time.hour, minutes=x.time.minute),
                                           Schedule.by_attribute(route_name, stop_name=stop_name_ya, _filter=_filter)))

                print(database_values)
                borders = get_nearest_actual_schedules(database_values, yandex_values[0])

                print(*yandex_values, borders)

                QueryRecord.create(request_time=datetime.now(),
                                   estimated_time=yandex_values[0],
                                   left_db_border=borders[0],
                                   right_db_border=borders[1])

            self.iterations_passed += 1
            print(self.iterations_passed)
            time.sleep(self.interval)


if __name__ == '__main__':
    create_database(['732'], fill_schedule_flag=True)
    handler = RemoteQueryPerformer(STOP_FIELDS[0]['stop_id'], '732', 30)
