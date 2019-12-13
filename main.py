from classes import *
import pprint


def get_selected_rows_list(_stop_name, _route=ROUTE_AB, _days=WORKDAYS):
    res = []
    query = TimetableDB.select().where(
        TimetableDB.route == _route,
        TimetableDB.days == _days,
    ).order_by(TimetableDB.stop_name)

    for row in query:
        if are_equals(row.stop_name, stop_name):
            res.append(row.arrival_time)
            # print(row.id, row.stop_name, row.arrival_time)

    return res


def get_estimated(rewrite_file=False):
    file = File(MAIN_STOP_JSON_FILENAME)
    if rewrite_file:
        file.write_json(proxy.get_stop_info(get_stop_url(MAIN_STOP_ID)))
    data = file.get_stop_schedules()

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(data)

    return data


start_time = time.time()

# main_db = Database(DB, [MAIN_BUS_NAME], _filter_days=[WORKDAYS])

stop_data_dict = get_estimated(rewrite_file=False)

stop_name = stop_data_dict[Tags.STOP_NAME]
estimated = stop_data_dict[MAIN_BUS_NAME][Tags.ESTIMATED]
print(stop_name)
print(estimated)

b = Bus("732")
# print(b.get_stops())
# print(b.get_stops())
print(list(b.get_timetable()) == b.get_stops())

exec_time = round(time.time() - start_time, 3)
print("Execution time :", round(time.time() - start_time, 3), "sec.")
