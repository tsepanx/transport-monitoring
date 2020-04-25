from datetime import datetime, date, time


def get_delta(a, b):
    x = datetime.combine(date.today(), a)
    y = datetime.combine(date.today(), b)
    res = abs(x - y)
    return (datetime.min + res).time()


def time_to_seconds(x):
    return x.hour * 60 * 60 + x.minute * 60 + x.second


def convert_time(value):
    return time(value.tm_hour, value.tm_min, value.tm_sec)