import datetime
from peewee import *
from constants import *

DB = SqliteDatabase(MAIN_DB_FILENAME)


def get_stop_url(id):
    return "https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__" + str(id)


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
    return distance(a, b) <= 3


def convert_time(value):
    return datetime.time(value.tm_hour, value.tm_min, value.tm_sec)


def pprint_time(t):
    s = ""
    s += str(t.hour) + ":" if t.hour > 0 else ""
    s += str(t.minute) + ":" if t.minute > 0 else ""
    s += str(t.second) if t.second > 0 else ""
    return s


def get_delta(a, b):

    x = datetime.datetime.combine(datetime.date.today(), a) - \
           datetime.datetime.combine(datetime.date.today(), b)
    return (datetime.datetime.min + x).time()
