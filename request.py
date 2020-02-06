import enum

from constants import GET_LINE_ID, proxy
from file import File
from parsers import parse_get_stop_info_json, parse_get_line_info_json

from database import YandexStop


def parse_request_obtained_json(sources, request_type):
    if request_type == Request.GET_STOP_INFO:
        return parse_get_stop_info_json(sources)
    elif request_type == Request.GET_LINE:
        return parse_get_line_info_json(sources)


def build_url(request_type, **kwargs):
    base_url = 'https://yandex.ru/maps/213/moscow/'

    res_url = base_url + ''

    if request_type == Request.GET_STOP_INFO:
        stop_id = str(kwargs['stop_id'])
        prefix = "?masstransit[stopId]="
        stop_url_prefix = "stop__" if len(stop_id) == 7 else ''

        res_url += prefix + stop_url_prefix + stop_id
    elif request_type == Request.GET_LINE:
        id = kwargs['line_id']
        thread_id = kwargs['thread_id']
        res_url += f"?&masstransit[lineId]={id}&masstransit[threadId]={thread_id}&mode=stop&z=18"

    print(res_url)
    return res_url


class YandexApiRequest:
    def __init__(self, request_type, **kwargs):
        self.request_type = request_type
        self.obtained_data = None
        self.file = None

    def run(self):
        yandex_api_func = self.request_type.value['func']
        raw_data = yandex_api_func(build_url(self.request_type, **self.url_args))

        self.obtained_data = parse_request_obtained_json(raw_data, self.request_type)

        return raw_data

    def write_to_file(self, data, suffix):
        self.file = File(self.request_type.value['file_prefix'] + suffix, "json")
        self.file.write_json(data)


class GetStopInfoApiRequest(YandexApiRequest):
    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.stop_name = None

        self.url_args = {'stop_id': stop_id}

        super().__init__(Request.GET_STOP_INFO, stop_id=stop_id)

    def run(self):
        data = super().run()
        self.stop_name = self.obtained_data['stopName']

        super().write_to_file(data, self.stop_id)

        self.__write_to_db()

    def __write_to_db(self):
        YandexStop.create(name_ya=self.stop_name, id_ya=self.stop_id)


class GetLineApiRequest(YandexApiRequest):
    def __init__(self, route_name):
        self.route_name = route_name
        self.url_args = GET_LINE_ID[route_name]
        super().__init__(Request.GET_LINE, route_name=route_name)

    def run(self):
        data = super().run()
        super().write_to_file(data, self.route_name)


class Request(enum.Enum):
    GET_STOP_INFO = {'func': proxy.get_stop_info, 'file_prefix': 'stop_'}
    GET_LINE = {'func': proxy.get_line, 'file_prefix': 'line_'}
