import os

from constants import ROUTES_FIELDS
from functions import *


class File:

    def __init__(self, filename, extension):
        self.full_name = get_full_filename(filename, extension)
        self.__extension = extension
        is_already_created = os.path.exists(self.full_name)

        self.__open("r" if is_already_created else "w+")
        print(self.full_name, self.__extension)

    def __open(self, _type):
        print(self.full_name)
        self.__file_object = open(self.full_name, _type)

    def raw_write(self, data):
        self.__open("w+")
        self.__file_object.write(data)

    def raw_read(self):
        self.__open("r")
        return self.__file_object.read()

    def raw_update(self, new_data: str):
        self.__open("+")
        prev_data = self.raw_read()
        self.raw_write(prev_data + "\n" + new_data)


class JsonFile(File):

    def __init__(self, route_name, request_type):
        self.request_type = request_type
        self.data_dict = {}

        super().__init__(self.request_type.value['prefix'] + route_name, "json")

    def write(self, data):
        d = convert(data)
        self.raw_write(d)

    def read(self):
        return json.loads(self.raw_read())

    def update(self, new_data: dict):
        self.raw_update(convert(new_data))


class YandexApiRequestFile(JsonFile):
    def __init__(self, request_type, route_name):
        super().__init__(route_name, request_type)
        self.url_args = ROUTES_FIELDS[route_name]

    def write_obtained_data(self):
        api_get_func = self.request_type.value['func']
        data = api_get_func(build_url(self.request_type, **self.url_args))
        self.write(data)
        self.data_dict = data
        return self
