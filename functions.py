import json
from datetime import datetime, date, time, timedelta


def convert(data: dict) -> str:
    return json.dumps(data, indent=2, separators=(',', ': '), default=str, ensure_ascii=False)


def is_today_workday():
    d = date.today().isoweekday()
    return 1 if d not in [6, 7] else 0


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
    i = len(expected_values) - 1
    while expected_values[i].hour > 0:
        expected_values[i] += timedelta(days=1)
        i -= 1

    if actual_value < expected_values[0]:
        return None, expected_values[0]

    if actual_value > expected_values[-1]:
        return expected_values[-1], None

    nearest_lower = binary_search_left(actual_value, expected_values)
    nearest_greater = nearest_lower + 1

    return nearest_lower, nearest_greater


def get_nearest_actual_schedules2(expected_values, actual_value):
    if expected_values[-1] <= actual_value <= expected_values[0]:
        return expected_values[-1], expected_values[0]

    for i, e in enumerate(expected_values):
        if actual_value >= e:
            return i, i + 1


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
    print(arr)
    res = binary_search_left(time(10, 20), arr)

    print(res, arr[res])


if __name__ == '__main__':
    main()
