from classes import *

proxy = MyYandexTransportProxy('127.0.0.1', 25555)

curr_bus = "732"
curr_stop_id = STOP_732_ID

file = GetStopInfoJsonFile(curr_bus, curr_stop_id).execute(proxy)
print_dict(file.data_dict)

manager = ServerManager(curr_bus, curr_stop_id, proxy)

while manager.main_thread.is_alive():
    pass

