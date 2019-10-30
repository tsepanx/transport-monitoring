from classes import *

fin = open("buses", "r")
buses = list(map(str.strip, fin.readlines()))

id = 0
while id < len(buses):
    bus_num = buses[id]
    b = Bus(bus_num)

    eq = (b.get_path(ROUTE_AB, WORKDAYS) == b.get_path(ROUTE_AB, WEEKENDS) and
          b.get_path(ROUTE_BA, WORKDAYS) == b.get_path(ROUTE_BA, WEEKENDS))

    print(bus_num, "__________________" if not eq else "")

    id += 1
