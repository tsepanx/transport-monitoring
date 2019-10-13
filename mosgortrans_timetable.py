from bs4 import BeautifulSoup
import requests
request = requests.get("http://www.mosgortrans.org/pass3/shedule.php?type=avto&way=732&date=1111100&direction=AB&waypoint=29")
soup = BeautifulSoup(''.join(request.text), features="html.parser")
timetable = soup.contents[0].contents[3].contents[1].contents[1].contents[4].contents[0].contents[0]
hours_list = soup.findAll('span', {'class': 'hour'})
minutes_list = timetable.findAll('td', {'align': 'left'})
list = [[0] * 20 for i in range(24)]
for i in range(len(minutes_list)):
    k = 0
    for j in range(0, len(minutes_list[i]), 3):
        if i >= len(hours_list):
            break
        list[int(hours_list[i].text)][j-2*k] = minutes_list[i].contents[j].text
        k += 1

for i in range(len(list)):
    for j in range(len(list[i])):
        if list[i][j] != 0:
            print(i, list[i][j])

