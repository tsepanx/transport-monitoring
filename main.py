from datetime import timedelta

from database import create_database, get_filtered_rows_from_db
from functions import convert
from request import YandexApiRequest, Request
from server import ServerManager


def run_server(route_name):
    duration = int(input("duration: "))
    interval = int(input("interval: "))

    manager = ServerManager(duration=timedelta(seconds=duration), interval=interval, route_name=route_name)

    while manager.main_thread.is_alive():
        pass


def run_requests(route_name):
    # request = YandexApiRequest(Request.GET_STOP_INFO, route_name)
    request = YandexApiRequest(Request.GET_LINE, route_name)

    request.run()
    print(convert(request.obtained_data))


def run_database_filter(route_name):
    # stop_id = ROUTES_FIELDS[route_name]['stop_id']
    stop_name = 'Давыдковская улица, 12'

    print(get_filtered_rows_from_db(route_name, stop_name))


def main():
    create_database(['104', '732'])

    route_name = '732'
    run_database_filter(route_name)


if __name__ == '__main__':
    main()
