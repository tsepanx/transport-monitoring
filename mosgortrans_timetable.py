from bs4 import BeautifulSoup
import requests
request = requests.get("http://www.mosgortrans.org/pass3/shedule.php?type=avto&way=732&date=1111100&direction=AB&waypoint=29")
soup = BeautifulSoup(''.join(request.text), features="html.parser")
timetable = soup.findAll('table', {'border': '0', 'cellspacing' : 0, 'cellpadding' : '0'})
hours_list = timetable[1].findAll('span', {'class': 'hour'})
minutes_list = timetable[1].findAll('td',  {'align': 'left'})
output = [[0] * 20 for i in range(24)]

grayhour_counter = 0
for i in range(len(minutes_list)):
    if len(minutes_list[i]) == 0:
        grayhour_counter += 1
    for j in minutes_list[i].findAll('span', {'class' : 'minutes'}):
        if i - grayhour_counter >= len(hours_list):
            break
        output[int(hours_list[i-grayhour_counter].text)].append(j.text)

for i in range(len(output)):
    for j in range(len(output[i])):
        if output[i][j] != 0:
            print(i, output[i][j])

