import requests
from bs4 import BeautifulSoup

WORKDAYS = "1111100"
WEEKENDS = "0000011"
ROUTE_AB = "AB"
ROUTE_BA = "BA"

def get_bus_timetable(bus_number=1):
    request = requests.get("http://www.mosgortrans.org/pass3/shedule.php?type=avto&way="+ str(bus_number) +"&date=1111100&direction=AB&waypoint=all")
    soup = BeautifulSoup(''.join(request.text), features="html.parser")

    h2 = soup.findAll('h2')
    h2.pop()
    for i in range(len(h2)): h2[i] = h2[i].text
    all_stations = dict.fromkeys(h2)

    timetable = soup.findAll('table', {'border': '0', 'cellspacing' : 0, 'cellpadding' : '0'})

    for i in range(1, len(timetable)):
        hours_list = timetable[i].findAll('span', {'class': 'hour'})
        minutes_list = timetable[i].findAll('td',  {'align': 'left'})
        output = [[0] * 8 for l in range(24)]
        gh_cnt = 0
        for g in range(len(minutes_list)):
            if minutes_list[g].find('span', {'class': 'minutes'}).text == "":
                gh_cnt += 1
                continue
            for j in minutes_list[g].findAll('span', {'class': 'minutes'}):
                if g - gh_cnt >= len(hours_list):
                    break
                output[int(hours_list[g-gh_cnt].text)].append(j.text)
        all_stations[h2[i-1]] = output

    for subj in all_stations:
        print('\n')
        print(subj)
        for i in range(len(all_stations[subj])):
            for j in range(len(all_stations[subj][i])):
                if all_stations[subj][i][j] != 0: print(i, all_stations[subj][i][j])

    return all_stations

def get_stops_list(bus_number=1, routes=[ROUTE_AB, ROUTE_BA], days=[WORKDAYS, WEEKENDS]):
    for day in days:
        for route in routes:
            raw_stops_list = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={bus_number}&date={day}&direction={route}')
            stops_list = []
            for stop in raw_stops_list.text.split('\n'):
                if stop == '':
                    break
                else:
                    stops_list.append(stop)
            print(bus_number, route, "weekdays" if day == WORKDAYS else "weekends", sep="\n")
            print(*stops_list, sep="\n")

bus_number = int(input())

get_bus_timetable(bus_number)
get_stops_list(bus_number)