from bs4 import BeautifulSoup
import requests

bus_number = input()

request = requests.get("http://www.mosgortrans.org/pass3/shedule.php?type=avto&way="+ bus_number +"&date=1111100&direction=AB&waypoint=all")
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

print(all_stations)