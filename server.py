from main import *

duration = int(input("duration"))
interval = int(input("interval"))

manager = ServerManager(curr_bus, curr_stop_id, proxy, interval=interval,
                        delta_time=datetime.timedelta(hours=duration))

while manager.main_thread.is_alive():
    pass
