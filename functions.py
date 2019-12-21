import json
import os
from datetime import datetime, date

from constants import PROJECT_PREFIX, FILENAMES_PREFIX, SHORT_STOP_ID_LENGTH, LONG_STOP_ID_LENGTH


def get_message_with_video_data(video_data):
    rows = []
    video_url = "https://www.youtube.com/watch?v=" + video_data["video_id"]

    rows.append(video_data["channel_title"])
    rows.append(video_data["video_title"])
    rows.append(video_data["video_comment_count"] + " comments")
    rows.append(video_data["video_like_count"] + " likes")
    rows.append(video_data["video_dislike_count"] + " dislikes")

    rows.append(str(video_data["video_publish_date"]))
    rows.append(video_url)

    return "\n".join(list(map(str, rows)))


def convert_dict_to_string(data: dict) -> str:
    return json.dumps(data, indent=2, separators=(',', ': '), default=str, ensure_ascii=False)


def print_near_times_data(route_name, stop_name, estimated, nearest_times):
    # stop_name = data_dict[Tags.STOP_NAME]
    # estimated = data_dict[route_name][Tags.ESTIMATED]

    print("================")
    print("===  ", route_name, "   ===")
    print("---", stop_name, "---")
    print()
    print("real value: ", estimated)
    print("db values: ", *nearest_times)
    print()
    print("Bus will come",
          get_delta(nearest_times[1], estimated),
          "earlier, \n or will be  ",
          get_delta(estimated, nearest_times[0]),
          "late")
    print("================")


def calculate_time_values_difference(times_list, db_list):
    estimated = times_list[0]

    nearest_times = []

    if db_list[-1] < estimated < db_list[0]:
        raise Exception("Buses are not available now!")

    for i, t in enumerate(db_list):
        if t >= estimated:
            nearest_times = [db_list[i - 1], t]
            break

    return nearest_times


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


# def print_dict(data):
#     pp = pprint.PrettyPrinter(indent=4, width=50)
#     pp.pprint(data)


def get_delta(a, b):
    x = datetime.combine(date.today(), a)
    y = datetime.combine(date.today(), b)
    res = abs(x - y)
    return (datetime.min + res).time()
