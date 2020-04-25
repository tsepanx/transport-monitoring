from src.constants import MY_DATABASE, DATABASE_PATH
from src.database.models import Filter, DATABASE_TIMETABLES_LIST, gather_schedule_sources, fill_schedule
from src.utils.file import does_exist

YA_MGT_STOPS_MATCHING = {
    'Давыдковская улица, 12': 'Давыдковская ул., 12'
}


def determine_same_stop_names(ya_name, mgt_name):
    if YA_MGT_STOPS_MATCHING.get(ya_name):
        return YA_MGT_STOPS_MATCHING[ya_name] == mgt_name or ya_name == mgt_name

    else:
        return ya_name == mgt_name


def create_database(routes_list, fill_schedule_flag=False, db=MY_DATABASE, _filter=Filter()):
    if not does_exist(DATABASE_PATH):
        db.create_tables(DATABASE_TIMETABLES_LIST)
    else:
        print("=== database already exists! ===")
        return

    if fill_schedule_flag:
        sources = gather_schedule_sources(routes_list, _filter)
        fill_schedule(sources)