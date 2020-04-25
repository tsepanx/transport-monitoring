from peewee import *

from src.constants import MY_DATABASE
from src.utils.functions import convert


class Filter:
    def __init__(self, way_filter=None, week_filter=None):
        self.ways = ("AB", "BA")
        self.days = ("1111100", "0000011")

        if isinstance(way_filter, str):
            self.way_filter = [way_filter]
        else:
            self.way_filter = self.ways if way_filter is None else [self.ways[way_filter]]

        if isinstance(week_filter, str):
            self.week_filter = [week_filter]
        else:
            self.week_filter = self.days if week_filter is None else [self.days[week_filter]]


class BaseModel(Model):
    class Meta:
        database = MY_DATABASE

    def __str__(self):
        return convert(vars(self)['__data__'])

    def __iter__(self):
        simple_attrs = vars(self)['__data__']
        rel_attrs = vars(self)['__rel__']

        for rel in rel_attrs:
            for simple_rel_attr in rel_attrs[rel]:
                yield simple_rel_attr

        for attr in simple_attrs:
            if attr not in ['id']:
                yield attr, simple_attrs[attr]


class RouteData(BaseModel):  # Buses
    name = CharField()


class YandexStop(BaseModel):
    name_ya = TextField()
    id_ya = IntegerField()


class StopData(BaseModel):
    name_mgt = CharField()
    route = ForeignKeyField(RouteData, related_name='bus', backref='stop')
    direction = CharField()

    ya_stop = ForeignKeyField(YandexStop, null=True, related_name='ya_stop', backref='stop')


class Schedule(BaseModel):
    stop = ForeignKeyField(StopData, related_name='stop', backref='schedule')
    weekdays = CharField()
    time = TimeField()

    @staticmethod
    def by_attribute(route_name, stop_id=None, stop_name=None, _filter=Filter()):
        def determine_same_stop_names(ya_name, mgt_name):
            YA_MGT_STOPS_MATCHING = {
                'Давыдковская улица, 12': 'Давыдковская ул., 12'
            }
            if YA_MGT_STOPS_MATCHING.get(ya_name):
                return YA_MGT_STOPS_MATCHING[ya_name] == mgt_name or ya_name == mgt_name
            else:
                return ya_name == mgt_name

        way = _filter.way_filter
        days = _filter.week_filter

        res = []
        query = Schedule.select().where(Schedule.weekdays << days)

        for row in query:
            if row.stop.direction in way:
                if (stop_id is not None) and stop_id != row.stop.id:
                    continue
                elif (stop_name is not None) and not determine_same_stop_names(stop_name, row.stop.name_mgt):
                    continue

                if row.stop.route.name == route_name:
                    res.append(row)

        return res


class QueryRecord(BaseModel):
    request_time = DateTimeField()
    bus_income = TimeField(null=True)
    left_db_border = TimeField(null=True)
    right_db_border = TimeField(null=True)
    timeout = IntegerField()
    stop_id = ForeignKeyField(StopData, null=True, related_name='stop', backref='queryrecord')


DATABASE_TIMETABLES_LIST = [Schedule, RouteData, StopData, QueryRecord, YandexStop]
