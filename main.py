from classes import *
import pprint

start_time = time.time()

# url = get_line_url("2036924115", "213A_641_bus_mosgortrans")

# vehicles info with region
# File("vehicles_641.json").write_json(proxy.get_vehicles_info_with_region(url_641))

main_db = Database(db, [MAIN_BUS])  # , _filter_days=[WORKDAYS])


def get_estimated(rewritefile=False):
    file = File(MAIN_STOP_JSON_FILENAME)
    if rewritefile:
        file.write_json(proxy.get_stop_info(get_stop_url(MAIN_STOP_ID)))
    data = file.get_stop_schedules()

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(data)


# get_estimated(True)

# line_url = get_line_url(MAIN_LINE_ID, MAIN_THREAD_ID)
#
# file = File(MAIN_LINE_JSON_FILENAME)
# file.write_json(proxy.get_line(get_line_url(MAIN_LINE_ID, MAIN_THREAD_ID)))

print("Execution time :", round(time.time() - start_time, 2), "sec.")
