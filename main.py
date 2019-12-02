from classes import *
import time

def init_database(raw_buses_list, filter_routes=(ROUTE_AB, ROUTE_BA), filter_days=(WORKDAYS, WEEKENDS)):
      db.create_tables([BusesDB, Time])
      
      for i in range(first_buses):
            data_source = []

            b = Bus(raw_buses_list[i])
            bus = BusesDB.create(name=raw_buses_list[i])
            b.get_timetable()
            for route in b.timetable:
                  for day in b.timetable[route]:
                        for stop_name in b.timetable[route][day]:
                              for time in b.timetable[route][day][stop_name]:
                                    print(b.name, route, day, stop_name, time)
                                    data_source.append((stop_name, bus, time, route, day))
                                    
                                    # time = Time.create(stop_name=stop_name, 
                                    # bus=bus, 
                                    # time=time, 
                                    # route=route, 
                                    # days=day)
            
            Time.insert_many(data_source, fields=[
                  Time.stop_name, 
                  Time.bus, 
                  Time.arrival_time, 
                  Time.route, 
                  Time.days]).execute()

# first_buses = 10
# buses_arr = []

# # x = make_url([55.937678999999996, 37.519211999999996])
# # print(x)
# fin = open("other/data4.json", "r")
# parsed_data = recursive_descent(json.loads(fin.read()))
# print(*parsed_data, sep="\n")
# db.connect()

x = time.localtime(1575267672)
print(x)

# BUSES_LIST_FILE_PATH = "other/buses"
# fin = open(BUSES_LIST_FILE_PATH, "r")
# buses = list(map(str.strip, fin.readlines()))

# init_database(buses) #, filter_routes=(ROUTE_AB), filter_days=(WORKDAYS))
