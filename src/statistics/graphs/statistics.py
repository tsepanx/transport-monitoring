import datetime

from src.utils.time import get_delta
from src.database.models import QueryRecord

records = QueryRecord.select().where(QueryRecord.bus_income is not None)

arr = {}

prev = None

for row in records:
    if prev:
        if prev.timeout < row.timeout:
            arr[prev.stop_id] = prev
    prev = row

lateness_dict_stops = {}


def average_of_massive_elements(massive):
    if len(massive) > 0:
        sum = 0
        for i in range(len(massive)):
            sum += massive[i]
        return sum / len(massive)
    else:
        return None


def get_stop_delay(stop_id, arr):
    lateness_list = []

    for i in arr:
        if get_delta(i.bus_income, i.left_db_border) <= get_delta(i.bus_income, i.right_db_border):
            lateness_list.append(get_delta(i.bus_income, i.left_db_border))
        else:
            lateness_list.append(get_delta(i.bus_income, i.right_db_border))

    lateness_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [],
                     13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: [], 21: [], 22: [], 23: []}
    count = 0

    for j in arr:
        lateness_dict[j.bus_income.hour].append(lateness_list[count])
        count += 1

    lateness_dict_seconds = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
                             12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: [], 21: [], 22: [],
                             23: []}

    for key in lateness_dict:
        for i in lateness_dict[key]:
            lateness_dict_seconds[key].append(
                datetime.timedelta(hours=i.hour, minutes=i.minute, seconds=i.second).total_seconds())

    lateness_dict_average_seconds = {}

    for i in range(24):
        lateness_dict_average_seconds[i] = average_of_massive_elements(lateness_dict_seconds[i])
    lateness_dict_stops[stop_id] = lateness_dict_average_seconds


print(lateness_dict_stops)
