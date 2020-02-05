import json
from datetime import datetime, date, time


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
    if actual_value < expected_values[0]:
        return None, expected_values[0]

    if actual_value > expected_values[-1]:
        return expected_values[-1], None

    nearest_lower = binary_search_left(actual_value, expected_values)
    nearest_greater = nearest_lower + 1

    return nearest_lower, nearest_greater


def convert_time(value):
    return time(value.tm_hour, value.tm_min, value.tm_sec)


def get_delta(a, b):
    x = datetime.combine(date.today(), a)
    y = datetime.combine(date.today(), b)
    res = abs(x - y)
    return (datetime.min + res).time()


def main():
    arr = sorted([1, 5, 7, 10, 20, 47, 80, 100, 45, 67, 35])
    print(arr)
    res = binary_search_left(int(input()), arr)

    print(res, arr[res])


if __name__ == '__main__':
    main()
