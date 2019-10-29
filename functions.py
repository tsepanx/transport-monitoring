import requests
from bs4 import BeautifulSoup

WORKDAYS = "1111100"
WEEKENDS = "0000011"
ROUTE_AB = "AB"
ROUTE_BA = "BA"

def time_convert(h, m):
    return h * 60 + m

def minutes_convert(m):
    h = m // 60
    return (h, m % 60)

def pretty_print_timetable(timetable):
    for stop_name in timetable:
        print(stop_name)
        arr = timetable[stop_name]

        print(list(map(minutes_convert, arr)), end="\n\n")

        # for i in range(len(arr)):
        #     print(minutes_convert(arr[i]), end=", ")
    # print()

def get_bus_timetable(bus_number="1", stop_filter="all"):
    request = requests.get(f"http://www.mosgortrans.org/pass3/shedule.php?type=avto&way={bus_number}&date=1111100&direction=AB&waypoint={stop_filter}")
    soup = BeautifulSoup(''.join(request.text), features="html.parser")

    stop_names = soup.findAll('h2')
    stop_names.pop()

    for i in range(len(stop_names)): stop_names[i] = stop_names[i].text
    res_dict = dict.fromkeys(stop_names)

    if stop_names == []:
        return False

    for i in res_dict.keys():
        res_dict[i] = []

    timetable = soup.findAll('table', {'border': '0', 'cellspacing' : 0, 'cellpadding' : '0'})

    for i in range(1, len(timetable)):
        hours_list = timetable[i].findAll('span', {'class': 'hour'})
        minutes_list = timetable[i].findAll('td',  {'align': 'left'})

        output = []
        gray_cnt = 0

        for g in range(len(minutes_list)):
            if minutes_list[g].find('span', {'class': 'minutes'}).text == "":
                gray_cnt += 1
                continue
            for j in minutes_list[g].findAll('span', {'class': 'minutes'}):
                if g - gray_cnt >= len(hours_list):
                    break

                hours = int(hours_list[g-gray_cnt].text)
                minutes = int(j.text)

                output.append(time_convert(hours, minutes))

        res_dict[stop_names[i-1]] = output

    return res_dict

def get_stops_list(bus_number="1", routes=[ROUTE_AB, ROUTE_BA], days=[WORKDAYS, WEEKENDS]):
    res = dict()

    for day in days:
        for route in routes:
            raw_stops_list = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={bus_number}&date={day}&direction={route}')
            stops_list = []
            for stop in raw_stops_list.text.split('\n'):
                if stop != "":
                    stops_list.append(stop)
            res[(route, day)] = stops_list

    return res