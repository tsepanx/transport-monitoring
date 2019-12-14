from classes import *


def loop_run(cnt=5, period=10):
    for i in range(cnt):
        print_bus_data(STOP_641_ID, "641")
        time.sleep(period)


def print_bus_data(stop_id, bus):
    file_732_stop = JsonFile(bus, _stop_id=stop_id)
    stop_data_dict = file_732_stop.execute()

    print_dict(stop_data_dict)

    stop_name = stop_data_dict[Tags.STOP_NAME]

    estimated_list = stop_data_dict[bus][Tags.ESTIMATED]
    scheduled_list = stop_data_dict[bus][Tags.SCHEDULED]
    if len(estimated_list + scheduled_list) == 0:
        exit("--- No buses on path now ---")

    estimated = (estimated_list + scheduled_list)[0]
    times_from_db = main_db.get_filtered_rows_from_db(bus, stop_name)

    nearest_times = []

    for i, t in enumerate(times_from_db):
        if t >= estimated:
            nearest_times = [times_from_db[i - 1], t]
            break

    print("================")
    print("===  ", bus, "   ===")
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
    print("================")


start_time = time.time()

main_db = Database(DB, ["27", "104", "732"], _filter_days=[TimetableFilter.WORKDAYS])
# main_db.execute() # --- fills db. use it only if you want to refill db

# print_bus_data(STOP_434_ID, "27")
print_bus_data(STOP_732_ID, "732")  # ---- main func

exec_time = round(time.time() - start_time, 3)

print()
print("Execution time :", exec_time, "sec.")
