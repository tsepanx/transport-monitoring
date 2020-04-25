import threading

from bottle import run

from src.constants import STOP_FIELDS
from src.functions import convert
from src.utils.request import GetStopInfoApiRequest, GetLineApiRequest, Request
from src.web import app

from src import server


def do_request(route_name, request_type=Request.GET_STOP_INFO):
    if request_type == Request.GET_STOP_INFO:
        request = GetStopInfoApiRequest(STOP_FIELDS[1]['stop_id'])
    elif request_type == Request.GET_LINE:
        request = GetLineApiRequest(route_name)
    else:
        raise Exception('Unknown request type')

    request.run()
    return request.obtained_data


def main_old():
    route_name = '732'

    # create_database([route_name, '104'], fill_schedule_flag=True)
    # print(convert(filter_database(route_name)))

    data = do_request(route_name, request_type=Request.GET_LINE)
    print(convert(data))


def main():
    threading.Thread(target=server.main()).start()
    run(app, host='localhost', port=3000)


if __name__ == '__main__':
    main()
