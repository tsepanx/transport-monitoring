import requests

bus_number = input()

WORKDAYS = "1111100"
WEEKENDS = "0000011"

def get_stops(bus_number, dirs, days):
    for day in days:
        for direction in dirs:
            stops = requests.get(f'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto&way={bus_number}&date={day}&direction={direction}')
            haltestellen = []
            for stop in stops.text.split('\n'):
                if stop == '':
                    break
                else:
                    haltestellen.append(stop)
            print(bus_number, direction, "weekdays" if day == WORKDAYS else "weekends", haltestellen, sep=" : ")

get_stops(bus_number, ["AB", "BA"], [WORKDAYS, WEEKENDS])