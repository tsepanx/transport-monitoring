bus_number = int(input())
from functions import *

stops = get_stops_list(bus_number)
timetable = get_bus_timetable(bus_number)

# pretty_print_timetable(timetable)
# print(*stops, sep="\n")
for i in stops:
    print(i)
    print(stops[i])
    print("-------")

# print(stops[(ROUTE_AB, WEEKENDS)] == stops[(ROUTE_AB, WORKDAYS)])
# print(stops[(ROUTE_BA, WEEKENDS)] == stops[(ROUTE_BA, WORKDAYS)])

n = 0
while n < 1100:

    if not get_bus_timetable(n):
        print(n, "lol")
        n += 1
        continue

    arr = get_stops_list(n)

    arr[(ROUTE_BA, WEEKENDS)].reverse()
    arr[(ROUTE_BA, WORKDAYS)].reverse()

    flag = True

    for i in arr.values():
        if i != arr[(ROUTE_AB, WEEKENDS)]:
            flag = False
            break
    
    print(n, " : ", flag)

    n += 1