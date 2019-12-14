from classes import *

start_time = time.time()

current_route = TimetableFilter.ROUTE_AB
current_day = TimetableFilter.WORKDAYS if is_today_workday() else TimetableFilter.WEEKENDS

print(current_route, current_day)

main_db = Database(DB, BUSES_LIST)  # , _filter_days=[TimetableFilter.WORKDAYS])
main_db.create()

# stop_file = GetStopInfoJsonFile("732", STOP_732_ID)
stop_file = GetStopInfoJsonFile("434", STOP_434_ID)
stop_file.execute()
stop_file.print_bus_data(main_db, current_route, current_day)

exec_time = round(time.time() - start_time, 3)

print()
print("Execution time :", exec_time, "sec.")
