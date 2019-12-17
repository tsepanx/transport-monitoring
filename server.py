from main import *

manager = ServerManager(curr_bus, curr_stop_id, proxy, interval=60,
                        delta_time=datetime.timedelta(hours=1))

while manager.main_thread.is_alive():
    pass
