import time

from functions import *
from constants import Tags, Request


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
        self.request_type = request_type  # Request.GET_STOP_INFO if _stop_id else Request.GET_LINE
        self.data_dict = dict()

        super().__init__(self.request_type.value + route_name, "json")

    def __init__(self, filename):
        self.data_dict = {}
        super().__init__(filename, "json")

    def write(self, data):
        d = convert_dict_to_string(data)
        self.raw_write(d)

    def read(self):
        return json.loads(self.raw_read())

    def update(self, new_data: dict):
        self.raw_update(convert_dict_to_string(new_data))


class GetStopInfoJsonFile(JsonFile):
    def __init__(self, route_name, stop_id):
        super().__init__(route_name, Request.GET_STOP_INFO)

        self.route_name = route_name
        self.stop_id = stop_id

    def execute(self, proxy):
        data = proxy.get_stop_info(get_stop_url(self.stop_id))
        self.write(data)

        self.data_dict = self.__get_transport_schedules()
        return self

    def __get_transport_schedules(self):
        data = self.read()

        res_dict = dict()

        props = data["data"]["properties"]
        stop_russian_fullname = props["name"]
        transport_data = props["StopMetaData"]["Transport"]

        res_dict[Tags.STOP_NAME] = stop_russian_fullname

        for route in transport_data:
            if route["type"] != "bus":
                continue

            name = route["name"]
            line_id = route[Tags.LINE_ID]

            res_dict[name] = {
                Tags.LINE_ID: line_id,
                Tags.THREAD_ID: [],

                Tags.SCHEDULED: [],
                Tags.ESTIMATED: [],
                Tags.FREQUENCY: None,

                Tags.ESSENTIAL_STOPS: []
            }

            threads = route["threads"]

            for thread in threads:
                thread_id = thread[Tags.THREAD_ID]
                schedules = thread[Tags.BRIEF_SCHEDULE]
                events = schedules[Tags.EVENTS]

                res_dict[name][Tags.THREAD_ID].append(thread_id)

                for event in events:
                    for tag in event:
                        if tag != "vehicleId":
                            value = time.localtime(int(event[tag]["value"]))
                            res_dict[name][tag].append(convert_time(value))

                if Tags.FREQUENCY in schedules:
                    frequency = schedules[Tags.FREQUENCY]["value"] // 60

                    first_arrival = time.localtime(int(schedules[Tags.FREQUENCY]["begin"]["value"]))
                    last_arrival = time.localtime(int(schedules[Tags.FREQUENCY]["end"]["value"]))

                    res_dict[name][Tags.FREQUENCY] = frequency
                    res_dict[name][Tags.ESSENTIAL_STOPS] = [convert_time(first_arrival), convert_time(last_arrival)]

        return res_dict


class GetLineJsonFile(JsonFile):
    def __init__(self, _line_id, _thread_id, route_name):
        self.line_id = _line_id
        self.thread_id = _thread_id

        super().__init__(route_name, Request.GET_LINE)

    def execute(self, proxy):
        data = proxy.get_line(get_line_url(self.line_id, self.thread_id))
        self.write(data)

        self.data_dict = self.__get_line_data()
        return self

    def __get_line_data(self):
        data = self.read()

        res_dict = {}

        stops_list = data["data"]["features"][0]["features"]

        for stop in stops_list:
            if Tags.PROPERTIES not in stop:
                continue

            properties = stop[Tags.PROPERTIES][Tags.STOP_META_DATA]
            name = properties["name"]
            raw_id = properties["id"]

            if "stop__" in raw_id:
                raw_id = int(raw_id[6:])
            else:
                raw_id = int(raw_id)

            res_dict[raw_id] = name

        return res_dict
