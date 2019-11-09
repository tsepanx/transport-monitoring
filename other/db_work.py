from peewee import *
from datetime import *

db = SqliteDatabase('people.db')

class Bus(Model):
    name = CharField()


    class Meta:
        database = db

class Time(Model):
    stop_name = CharField()
    bus = ForeignKeyField(Bus, related_name="bus")
    time = TimeField()
    

    class Meta:
        database = db


db.connect()
db.create_tables([Bus, Time])

bus1 = Bus.create(id=1, name="101")
bus2 = Bus.create(id=300, name="200")

time1 = Time.create(id=1, stop_name="lol", bus=bus2, time=time(hour=5, minute=36))