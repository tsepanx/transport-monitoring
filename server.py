from main import *

duration = int(input("duration: "))
interval = int(input("interval: "))

manager = ServerManager(current_route_name, current_stop_id, proxy, interval=interval,
                        delta_time=timedelta(hours=duration))

while manager.main_thread.is_alive():
    pass
