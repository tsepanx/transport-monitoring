from constants import does_exist, PROJECT_PREFIX

import peewee as pw

from functions import convert

db_path = PROJECT_PREFIX + 'transport'
db = pw.PostgresqlDatabase(db_path)


class BaseModel(pw.Model):
    class Meta:
        database = db

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


class QueryRecord(BaseModel):
    request_time = pw.DateTimeField()
    bus_income = pw.TimeField(null=True)
    left_db_border = pw.TimeField(null=True)
    right_db_border = pw.TimeField(null=True)
    timeout = pw.IntegerField()


if __name__ == '__main__':
    tables = [QueryRecord]

    if not does_exist(db_path):
        db.create_tables(tables)
