import json
import os

from src.constants import PROJECT_PREFIX, GENERATED_DIR
from src.utils.functions import convert


class File:
    def __init__(self, filename, extension):
        self.full_name = get_full_filename(filename, extension)
        self.__extension = extension
        is_already_created = os.path.exists(self.full_name)

        self.__open("r" if is_already_created else "w+")

    def __open(self, _type):
        print(self.full_name, self.__extension, "'open'", _type)
        self.__file_object = open(self.full_name, _type)

    def __write(self, data):
        self.__open("w+")
        self.__file_object.write(data)

    def __read(self):
        self.__open("r")
        return self.__file_object.read()

    def __update(self, new_data: str):
        self.__open("+")
        prev_data = self.__read()
        self.__write(prev_data + "\n" + new_data)

    def write_json(self, data: dict):
        d = convert(data)
        self.__write(d)

    def read_json(self):
        return json.loads(self.__read())


def does_exist(path):
    return os.path.exists(path)


def create_if_not_exists(path):
    print(path)
    if not does_exist(path):
        print('Creating ', path)
        os.mkdir(path)


def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def get_full_filename(filename, ext="json"):
    return PROJECT_PREFIX + GENERATED_DIR + filename + "." + ext