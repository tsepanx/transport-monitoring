import json
import os
from datetime import datetime, date, time

from constants import PROJECT_PREFIX, FILENAMES_PREFIX, SHORT_STOP_ID_LENGTH, LONG_STOP_ID_LENGTH


class JsonSerializable(dict):

    def __init__(self, s: str):
        super().__init__()
        self.__class__ = json.loads(s)

    def __str__(self):
        return convert(self)


def convert(data: dict) -> str:
    return json.dumps(data, indent=2, separators=(',', ': '), default=str, ensure_ascii=False)


def get_closest_values(x, arr):
    for i, t in enumerate(arr):
        if t >= x:
            return [arr[i - 1], t]


def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def is_today_workday():
    d = date.today().isoweekday()
    return 1 if d not in [6, 7] else 0


def get_full_filename(filename, ext="json"):
    return PROJECT_PREFIX + FILENAMES_PREFIX + filename + "." + ext


def get_stop_url(id):
    stop_url_prefix = "stop__"
    prefix = "https://yandex.ru/maps/213/moscow/?masstransit[stopId]="
    s = str(id)
    if len(s) == SHORT_STOP_ID_LENGTH:
        return prefix + stop_url_prefix + s
    elif len(s) == LONG_STOP_ID_LENGTH:
        return prefix + s
    else:
        raise Exception("Another stop id length found")


def get_line_url(id, thread_id):
    return f"https://yandex.ru/maps/213/moscow/?&masstransit[lineId]={id}&masstransit[threadId]={thread_id}&mode=stop&z=18"


def lewen_length(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def convert_time(value):
    return time(value.tm_hour, value.tm_min, value.tm_sec)


def get_delta(a, b):
    x = datetime.combine(date.today(), a)
    y = datetime.combine(date.today(), b)
    res = abs(x - y)
    return (datetime.min + res).time()
