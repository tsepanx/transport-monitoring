import requests

r = requests.get('http://www.mosgortrans.org/pass3/request.ajax.php?list=ways&type=avto')
directions = ['AB', 'BA']
for i in r.text.split():
    days = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=days&type=avto&way={i}')
    for day in days.text.split():
                for direction in directions:
                    bushaltestellen = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={i}&date={day}&direction={direction}')
                    haltestellen = []
                    for bushaltestelle in bushaltestellen.text.split('\n'):
                        if bushaltestelle == '':
                            break
                        else:
                            haltestellen.append(bushaltestelle)
    print(i, ':', haltestellen)