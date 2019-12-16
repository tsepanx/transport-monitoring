from classes import *


def main_func(bus, stop):
    current_route = TimetableFilter.ROUTE_AB
    current_day = TimetableFilter.WORKDAYS if is_today_workday() else TimetableFilter.WEEKENDS

    print(current_route, current_day)

    db = Database(BUSES_LIST).create()

    stop_file = GetStopInfoJsonFile(curr_bus, stop).execute(proxy)
    stop_file.print_bus_data(current_route, current_day)

    line_id = stop_file.data_dict[bus][Tags.LINE_ID]
    thread_id = stop_file.data_dict[bus][Tags.THREAD_ID][0]

    print(line_id, thread_id)

    line_file = GetLineJsonFile(line_id, thread_id, bus).execute(proxy)
    print_dict(line_file.data_dict)

start_time = time.time()
proxy = MyYandexTransportProxy('127.0.0.1', 25555)

curr_bus = "732"
curr_stop = STOP_732_ID

if __name__ == '__main__':
    main_func(curr_bus, curr_stop)

exec_time = round(time.time() - start_time, 3)

print()
print("Execution time :", exec_time, "sec.")
