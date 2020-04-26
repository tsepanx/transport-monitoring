import threading

from bottle import run

from src.constants import PROJECT_PREFIX, GENERATED_DIR, proxy
from src.utils import server
from src.utils.file import create_if_not_exists
from src.utils.functions import convert
from src.utils.request import do_request, RequestEnum
from src.web.web import app


def main_old():
    route_name = '732'

    # create_database([route_name, '104'], fill_schedule_flag=True)
    # print(convert(filter_database(route_name)))

    # data = do_request(route_name, request_type=RequestEnum.GET_STOP_INFO)
    # print(convert(data))
    # proxy.get_stop_info('https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__9650244', blocking=False)


def main():
    # Start doing requests
    threading.Thread(target=server.main()).start()

    # Run the web
    run(app, host='localhost', port=3000)


if __name__ == '__main__':
    create_if_not_exists(PROJECT_PREFIX + GENERATED_DIR)
    main()
    # main_old()
