from classes import *

start_time = time.time()

current_route = TimetableFilter.ROUTE_AB
current_day = TimetableFilter.WORKDAYS if is_today_workday() else TimetableFilter.WEEKENDS

print(current_route, current_day)

main_db = Database(DB, BUSES_LIST).create()

curr_bus = "732"
curr_stop = STOP_732_ID

stop_file = GetStopInfoJsonFile(curr_bus, curr_stop).execute()

stop_file.print_bus_data(main_db, current_route, current_day)

line_id = stop_file.data_dict[curr_bus][Tags.LINE_ID]
thread_id = stop_file.data_dict[curr_bus][Tags.THREAD_ID][0]

print(line_id, thread_id)

line_file = GetLineJsonFile(line_id, thread_id, curr_bus).execute()
print_dict(line_file.data_dict)

exec_time = round(time.time() - start_time, 3)

print()
print("Execution time :", exec_time, "sec.")
