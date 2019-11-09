from peewee import *
from datetime import *

db = SqliteDatabase('people.db')

class Bus(Model):
    # id = IntegerField()
    name = CharField()


    class Meta:
        database = db

class Time(Model):
    # id = IntegerField()
    stop_name = CharField()
    bus = ForeignKeyField(Bus, related_name="bus")
    time = DateField()
    

    class Meta:
        database = db


db.connect()
db.create_tables([Bus, Time])

bus1 = Bus.create(id=1, name="101")
bus2 = Bus.create(id=300, name="200")

time1 = Time.create(id=1, stop_name="lol", bus=bus2, time=date(2019, 1, 1))