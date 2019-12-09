from constants import *
from peewee import *
from yandex_transport_webdriver_api import YandexTransportProxy

proxy = YandexTransportProxy('127.0.0.1', 25555)


def get_stop_url(id):
    return "https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__" + str(id)


def get_line_url(id, thread_id):
    return f"https://yandex.ru/maps/213/moscow/?ll=37.679549,55.772203&masstransit[lineId]={id}&masstransit[threadId]={thread_id}&mode=stop&z=18"


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


def pretty_time(time_struct):
    return ":".join(map(str, [time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec]))
