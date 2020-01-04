import json
from datetime import datetime, date, time

from constants import PROJECT_PREFIX, GENERATED_DIR, Request


class JsonSerializable(dict):

    def __init__(self, s: str):
        super().__init__()
        self.__class__ = json.loads(s)

    def __str__(self):
        return convert(self)


def convert(data: dict) -> str:
    return json.dumps(data, indent=2, separators=(',', ': '), default=str, ensure_ascii=False)


def is_today_workday():
    d = date.today().isoweekday()
    return 1 if d not in [6, 7] else 0


def get_full_filename(filename, ext="json"):
    return PROJECT_PREFIX + GENERATED_DIR + filename + "." + ext


def build_url(request_type, **kwargs):
    base_url = 'https://yandex.ru/maps/213/moscow/'

    res_url = base_url + ''

    if request_type == Request.GET_STOP_INFO:
        stop_id = str(kwargs['stop_id'])
        prefix = "?masstransit[stopId]="
        stop_url_prefix = "stop__" if len(stop_id) == 7 else ''

        res_url += prefix + stop_url_prefix + stop_id
    elif request_type == Request.GET_LINE:
        id = kwargs['line_id']
        thread_id = kwargs['thread_id']
        res_url += f"?&masstransit[lineId]={id}&masstransit[threadId]={thread_id}&mode=stop&z=18"

    print(res_url)
    return res_url


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
