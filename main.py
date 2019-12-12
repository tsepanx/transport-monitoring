from classes import *
import pprint


def get_selected_rows_list(_stop_name, _route=ROUTE_AB, _days=WORKDAYS):
    return Time.select().where(
        Time.route == _route,
        Time.days == _days,
    ).order_by(Time.stop_name)


def get_estimated(rewrite_file=False):
    file = File(MAIN_STOP_JSON_FILENAME)
    if rewrite_file:
        file.write_json(proxy.get_stop_info(get_stop_url(MAIN_STOP_ID)))
    data = file.get_stop_schedules()

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(data)

    return data


start_time = time.time()

# main_db = Database(DB, [MAIN_BUS])  # , _filter_days=[WORKDAYS])

stop_data_dict = get_estimated(rewrite_file=False)

stop_name = stop_data_dict[Tags.STOP_NAME]
estimated = stop_data_dict[MAIN_BUS_NAME][Tags.ESTIMATED]
print(stop_name)
print(estimated)

db_filtered_times = []

for row in get_selected_rows_list(stop_name):
    if are_equals(row.stop_name, stop_name):
        db_filtered_times.append(row.arrival_time)
        print(row.id, row.stop_name, row.arrival_time)

print(*db_filtered_times, sep="\n")

print("Execution time :", round(time.time() - start_time, 3), "sec.")
