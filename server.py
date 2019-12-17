from main import *

manager = ServerManager(curr_bus, curr_stop_id, proxy)

while manager.main_thread.is_alive():
    pass
