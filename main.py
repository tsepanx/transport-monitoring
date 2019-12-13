from classes import *
import pprint


def get_filtered_rows_list(_stop_name, _route=TimetableFilter.ROUTE_AB, _days=TimetableFilter.WORKDAYS):
    res = []
    query = TimetableDB.select().where(
        TimetableDB.route == _route,
        TimetableDB.days == _days,
    ).order_by(TimetableDB.stop_name)

    for row in query:
        if are_equals(row.stop_name, stop_name):
            res.append(row.arrival_time)

    return res


def get_estimated(rewrite_file=False, _pprint=False):
    file = File(MAIN_STOP_JSON_FILENAME)
    if rewrite_file:
        file.write_json(proxy.get_stop_info(get_stop_url(MAIN_STOP_ID)))
    data = file.get_stop_schedules()

    if _pprint:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(data)

    return data


start_time = time.time()

main_db = Database(DB, [MAIN_BUS_NAME], _filter_days=[TimetableFilter.WORKDAYS])
# main_db.execute()

stop_data_dict = get_estimated(rewrite_file=True, _pprint=True)

stop_name = stop_data_dict[Tags.STOP_NAME]

estimated = stop_data_dict[MAIN_BUS_NAME][Tags.ESTIMATED][0]
times_from_db = get_filtered_rows_list(stop_name)

nearest_times = []

for i, t in enumerate(times_from_db):
    if t >= estimated:
        nearest_times = [times_from_db[i - 1], t]
        break

exec_time = round(time.time() - start_time, 3)

print("---", stop_name, "---")
print("real value: ", estimated)
print("db values: ", *nearest_times)
print()
print("Bus will come",
      get_delta(estimated, nearest_times[0]),
      " earlier, or will be",
      get_delta(nearest_times[1], estimated),
      "late")

print("Execution time :", exec_time, "sec.")
