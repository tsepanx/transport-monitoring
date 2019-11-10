from classes import *

first_buses = 1

buses_arr = []

def init_database(raw_buses_list):
      db.connect()
      db.create_tables([BusesDB, Time])
      
      for i in range(first_buses):
            b = Bus(raw_buses_list[i])
            bus = BusesDB.create(name=raw_buses_list[i])
            b.get_all_timetable()
            for route in b.timetable:
                  for day in b.timetable[route]:
                        for stop_name in b.timetable[route][day]:
                              for time in b.timetable[route][day][stop_name]:
                                    print(b.name, route, day, stop_name, time)
                                    time = Time.create(stop_name=stop_name, 
                                    bus=bus, 
                                    time=time, 
                                    route=route, 
                                    days=day)

BUSES_LIST_FILE_PATH = "other/buses"

fin = open(BUSES_LIST_FILE_PATH, "r")
buses = list(map(str.strip, fin.readlines()))

init_database(buses)

# id = 0
# while id < len(buses):
#     bus_num = buses[id]
#     b = Bus(bus_num)

#     eq = (b.get_path(ROUTE_AB, WORKDAYS) == b.get_path(ROUTE_AB, WEEKENDS) and
#           b.get_path(ROUTE_BA, WORKDAYS) == b.get_path(ROUTE_BA, WEEKENDS))

#     print(bus_num, "__________________" if not eq else "")

#     id += 1
