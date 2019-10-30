from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # this model uses the "people.db" database

db.connect()
db.create_tables([Person])
