from classes import *

start_time = time.time()

main_db = Database(DB, ["104", "732"], _filter_days=[TimetableFilter.WORKDAYS])
# main_db.execute()

file_732_stop = JsonFile(MAIN_BUS_NAME, _stop_id=MAIN_STOP_ID)
stop_data_dict = file_732_stop.execute()
print_dict(stop_data_dict)

stop_name = stop_data_dict[Tags.STOP_NAME]

estimated_list = stop_data_dict[MAIN_BUS_NAME][Tags.ESTIMATED]
scheduled_list = stop_data_dict[MAIN_BUS_NAME][Tags.SCHEDULED]
if len(estimated_list + scheduled_list) == 0:
    exit("--- No buses on path now ---")

estimated = (estimated_list + scheduled_list)[0]
times_from_db = main_db.get_filtered_rows_from_db(MAIN_BUS_NAME, stop_name)

nearest_times = []

for i, t in enumerate(times_from_db):
    if t >= estimated:
        nearest_times = [times_from_db[i - 1], t]
        break

exec_time = round(time.time() - start_time, 3)

print("---", stop_name, "---")
print()
print("real value: ", estimated)
print("db values: ", *nearest_times)  # , sep="\n")
print()
print("Bus will come",
      get_delta(nearest_times[1], estimated),
      "earlier, \n or will be  ",
      get_delta(estimated, nearest_times[0]),
      "late")

print()
print("Execution time :", exec_time, "sec.")
