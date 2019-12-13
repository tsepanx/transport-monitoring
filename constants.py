FILENAMES_PREFIX = "generated_files/"
PROJECT_PREFIX = "/home/stepan/TransportMonitoring/"

MAIN_BUS_NAME = "732"
MAIN_STOP_JSON_FILENAME = "stop_732.json"
MAIN_STOP_METRO_JSON_FILENAME = "stop_732_metro.json"
MAIN_LINE_JSON_FILENAME = "line_732.json"
MAIN_DB_FILENAME = "732.db"

MAIN_STOP_ID = 9644642  # Давыдковская улица, 10
MAIN_LINE_ID = "213_732_bus_mosgortrans"
MAIN_THREAD_ID = "213A_732_bus_mosgortrans"

STOP_641_ID = 9644493
STOP_434_ID = 10110344


class Tags:
    STOP_NAME = "stopName"

    BRIEF_SCHEDULE = "BriefSchedule"
    THREAD_ID = "threadId"
    LINE_ID = "lineId"

    EVENTS = "Events"

    ESTIMATED = "Estimated"
    SCHEDULED = "Scheduled"

    ESSENTIAL_STOPS = "EssentialStops"

    FREQUENCY = "Frequency"


class TimetableFilter:
    WORKDAYS = "1111100"
    WEEKENDS = "0000011"
    ROUTE_AB = "AB"
    ROUTE_BA = "BA"

    ROUTES = (ROUTE_AB, ROUTE_BA)
    DAYS = (WORKDAYS, WEEKENDS)
