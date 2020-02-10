import json
from datetime import datetime, date, time


def convert(data: dict) -> str:
    return json.dumps(data, indent=2, separators=(',', ': '), default=str, ensure_ascii=False)


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

    print(int_values)

    return nearest_lower, nearest_greater


def convert_time(value):
    return time(value.tm_hour, value.tm_min, value.tm_sec)


def get_delta(a, b):
    x = datetime.combine(date.today(), a)
    y = datetime.combine(date.today(), b)
    res = abs(x - y)
    return (datetime.min + res).time()


def main():
    # arr = sorted([1, 5, 7, 10, 20, 47, 80, 100, 45, 67, 35])
    arr = [time(5, 50), time(6, 10), time(6, 30), time(6, 50), time(7, 2), time(7, 19), time(7, 33), time(7, 48),
           time(8, 1), time(8, 15), time(8, 28), time(8, 41), time(8, 54), time(9, 5), time(9, 15), time(9, 26),
           time(9, 39), time(9, 54), time(10, 9), time(10, 24), time(10, 39), time(10, 54), time(11, 9), time(11, 24),
           time(11, 39), time(11, 54), time(12, 9), time(12, 24), time(12, 39), time(12, 54), time(13, 9), time(13, 24),
           time(13, 39), time(13, 54), time(14, 9), time(14, 24), time(14, 39), time(14, 54), time(15, 11),
           time(15, 27), time(15, 44), time(16, 5), time(16, 25), time(16, 45), time(17, 5), time(17, 25), time(17, 45),
           time(18, 5), time(18, 17), time(18, 29), time(18, 41), time(18, 53), time(19, 4), time(19, 12), time(19, 23),
           time(19, 34), time(19, 45), time(20, 4), time(20, 24), time(20, 44), time(21, 4), time(21, 21), time(21, 38),
           time(21, 57), time(22, 27), time(22, 57), time(23, 27), time(23, 57), time(0, 27), time(0, 57), time(1, 27),
           time(1, 57)]

    res = get_nearest_actual_schedules(arr, time(1, 40))

    print(res)


if __name__ == '__main__':
    main()
