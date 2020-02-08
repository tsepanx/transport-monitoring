from constants import STOP_FIELDS
from database import Schedule, Filter, StopData
from functions import convert
from request import GetStopInfoApiRequest, GetLineApiRequest, Request
from server import RemoteQueryPerformer


def run_remote_executor(route_name):
    interval = int(input("interval: "))

    performer = RemoteQueryPerformer(interval=interval, route_name=route_name)

    while performer.main_thread.is_alive():
        pass


def do_request(route_name, request_type=Request.GET_STOP_INFO):
    if request_type == Request.GET_STOP_INFO:
        request = GetStopInfoApiRequest(STOP_FIELDS[1]['stop_id'])
    elif request_type == Request.GET_LINE:
        request = GetLineApiRequest(route_name)
    else:
        raise Exception('Unknown request type')

    request.run()
    return request.obtained_data


# def filter_database(route_name, stop_id):
#     return Schedule.by_stop_id(route_name, stop_id)


def main():
    route_name = '732'

    # create_database([route_name, '104'], fill_schedule_flag=True)
    # print(convert(filter_database(route_name)))

    data = do_request(route_name, request_type=Request.GET_LINE)
    print(convert(data))


if __name__ == '__main__':
    main()
