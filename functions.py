import datetime
import pprint
from constants import *


def is_today_workday():
    d = datetime.date.today().isoweekday()
    print(d)
    return d not in [6, 7]


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


def recursive_descent(data):
    res = []
    cur = []

    if type(data) == type(dict()):
        for i in data:
            cur.append(data[i])
    else:
        cur = data

    if len(cur) == 2:
        if list(map(type, cur)) == [type(float())] * 2:
            return [cur]

    for x in cur:
        if type(x) in [type([]), type(dict())]:
            z = recursive_descent(x)
            res.extend(z)

    return res


def distance(a, b):
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


def are_equals(a, b):
    return distance(a, b) <= 5


def convert_time(value):
    return datetime.time(value.tm_hour, value.tm_min, value.tm_sec)


def print_dict(data):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(data)


def get_delta(a, b):
    x = datetime.datetime.combine(datetime.date.today(), a)
    y = datetime.datetime.combine(datetime.date.today(), b)
    res = abs(x - y)
    # print(x, y, res)
    return (datetime.datetime.min + res).time()
