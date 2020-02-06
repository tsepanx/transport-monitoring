import time

from functions import convert_time


class Tags:
    STOP_NAME = "stopName"

    BRIEF_SCHEDULE = "BriefSchedule"

    STOP_ID = 'stopId'
    THREAD_ID = "threadId"
    LINE_ID = "lineId"

    EVENTS = "Events"

    ESTIMATED = "Estimated"
    SCHEDULED = "Scheduled"

    ESSENTIAL_STOPS = "EssentialStops"

    FREQUENCY = "Frequency"

    STOP_META_DATA = "StopMetaData"
    PROPERTIES = "properties"


def parse_get_stop_info_json(sources):
    res_dict = dict()

    props = sources["data"][Tags.PROPERTIES]
    stop_russian_fullname = props["name"]
    transport_data = props[Tags.STOP_META_DATA]["Transport"]

    res_dict[Tags.STOP_NAME] = stop_russian_fullname
    res_dict[Tags.STOP_ID] = int(props[Tags.STOP_META_DATA]['id'][6:])

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


def parse_get_line_info_json(sources):
    res_dict = {}

    stops_list = sources["data"]["features"][0]["features"]

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
