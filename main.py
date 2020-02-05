from database import create_database, ArrivalTime, Filter
from functions import convert
from request import YandexApiRequest, Request
from server import RemoteQueryPerformer


def run_remote_executor(route_name):
    interval = int(input("interval: "))

    performer = RemoteQueryPerformer(interval=interval, route_name=route_name)

    while performer.main_thread.is_alive():
        pass


def do_request(route_name, request_type=Request.GET_LINE):
    request = YandexApiRequest(request_type, route_name)

    request.run()
    print(convert(request.obtained_data))


def filter_database(route_name):
    stop_name = 'Давыдковская улица, 12'

    print(ArrivalTime.by_stop_name(route_name, stop_name, Filter(week_filter=0)))


def main():
    create_database(['104', '732'])

    route_name = '732'
    filter_database(route_name)
    do_request(route_name, request_type=Request.GET_STOP_INFO)


if __name__ == '__main__':
    main()
