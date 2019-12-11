from classes import *

start_time = time.time()

# url = get_line_url("2036924115", "213A_641_bus_mosgortrans")

# vehicles info with region
# File("vehicles_641.json").write_json(proxy.get_vehicles_info_with_region(url_641))

# main_db = Database(db, [MAIN_BUS])


file = File(MAIN_STOP_JSON_FILENAME)
file.write_json(proxy.get_stop_info(get_stop_url(MAIN_STOP_ID)))
file.get_stop_schedules()

print(get_line_url(MAIN_LINE_ID, MAIN_THREAD_ID))

print("Execution time :", round(time.time() - start_time, 2), "sec.")