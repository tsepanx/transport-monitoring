from classes import *

start_time = time.time()

main_db = Database(DB, BUSES_LIST, _filter_days=[TimetableFilter.WORKDAYS])
# main_db.execute() # --- fills db. use it only if you want to refill db

stop_file = GetStopInfoJsonFile("732", STOP_732_ID)
stop_file.print_bus_data(main_db)

exec_time = round(time.time() - start_time, 3)

print()
print("Execution time :", exec_time, "sec.")
