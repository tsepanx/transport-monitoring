from functions import convert
from request import YandexApiRequest, Request
from classes import create_database


def main():
    create_database(['104', '732'])

    request = YandexApiRequest(Request.GET_STOP_INFO, '732')
    # request = YandexApiRequest(Request.GET_LINE, '732')  # TODO doesnt work

    request.run()

    print(convert(request.obtained_data))


if __name__ == '__main__':
    main()
