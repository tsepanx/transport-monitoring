from classes import *

proxy = MyYandexTransportProxy('127.0.0.1', 25555)

curr_bus = "732"
curr_stop_id = STOP_732_ID

if __name__ == '__main__':
    Database(BUSES_LIST).create()

    file = GetStopInfoJsonFile(curr_bus, curr_stop_id).execute(proxy)
    print_dict(file.data_dict)
    # print_near_times_data(curr_bus,
    #                       file.data_dict[Tags.STOP_NAME],
    #                       file.data_dict[curr_bus][Tags.ESTIMATED],
    #                       )
