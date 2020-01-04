from constants import Request, ROUTES_FIELDS
from file import File
from functions import convert, build_url


class YandexApiRequest:
    def __init__(self, request_type, route_name):
        self.request_type = request_type
        self.route_name = route_name
        self.url_args = ROUTES_FIELDS[route_name]
        self.obtained_data = None
        self.file = None

        # self.run()

    def run(self):
        api_get_func = self.request_type.value['func']
        self.obtained_data = api_get_func(build_url(self.request_type, **self.url_args))

    def write_to_file(self):
        self.file = File(self.request_type.value['prefix'] + self.route_name, "json")
        self.file.write_json(self.obtained_data)


def main():
    request = YandexApiRequest(Request.GET_STOP_INFO, '732')
    # request = YandexApiRequest(Request.GET_LINE, '732')

    request.run()

    print(convert(request.obtained_data))


if __name__ == '__main__':
    main()
