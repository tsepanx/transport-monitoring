from database import create_database, Schedule, Filter
from functions import convert
from request import GetStopInfoApiRequest, Request
from server import RemoteQueryPerformer


def run_remote_executor(route_name):
    interval = int(input("interval: "))

    performer = RemoteQueryPerformer(interval=interval, route_name=route_name)

    while performer.main_thread.is_alive():
        pass


def do_request(route_name, request_type=Request.GET_STOP_INFO):
    if request_type == Request.GET_STOP_INFO:
        request = GetStopInfoApiRequest(route_name)
    elif request_type == Request.GET_LINE:
        request = GetStopInfoApiRequest(route_name)
    else:
        raise Exception('Unknown request type')

    request.run()
    print(convert(request.obtained_data))


def filter_database(route_name):
    stop_name = 'Давыдковская улица, 12'

    print(Schedule.by_stop_name(route_name, stop_name, Filter(week_filter=0)))


def main():
    route_name = '732'
    create_database([route_name], fill_schedule=False, _filter=Filter(0, 0))
    # filter_database(route_name)

    do_request(route_name, request_type=Request.GET_STOP_INFO)


if __name__ == '__main__':
    main()
