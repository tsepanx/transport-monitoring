from constants import routes_fields, proxy
from file import GetStopInfoJsonFile
from functions import convert


def main():
    current_route_name = "732"
    current_stop_id = routes_fields[current_route_name]['main_stop_id']

    file = GetStopInfoJsonFile(current_route_name, current_stop_id).execute(proxy)
    print(convert(file.data_dict))


if __name__ == '__main__':
    main()
