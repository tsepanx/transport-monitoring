from functions import *

fin = open("buses", "r")
buses = list(map(str.strip, fin.readlines()))[1:]

id = 0
while id < len(buses):
    
    n = buses[id]

    tt = get_bus_timetable(n)
    if not tt:
        print(n, "Bus Doesn't exist!")
        id += 1
        continue

    stops_tt = [i for i in tt]
    stops = get_stops_list(n)

    stops[(ROUTE_BA, WEEKENDS)].reverse()
    stops[(ROUTE_BA, WORKDAYS)].reverse()

    types_stops = [i for i in stops.values()]
    
    print(n)

    for i in types_stops:
        print(len(i), end=" : ")
    print("\n")
    
    id += 1