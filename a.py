from functions import *

fin = open("buses", "r")
buses = list(map(str.strip, fin.readlines()))[1:]

print(buses)

# stops = get_stops_list(bus_number, ROUTE_AB, WORKDAYS)
# timetable = get_bus_timetable(bus_number, 0)

# pretty_print_timetable(timetable)
# print(*stops, sep="\n")

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

    flag = True

    for i in stops.values():
        i1 = stops[(ROUTE_AB, WORKDAYS)]
        # print(i, i1)
        if i != i1:
            flag = False
            break
    
    print(n, flag, len(stops[(ROUTE_AB, WORKDAYS)]), len(stops_tt), sep=" : ")
    id += 1