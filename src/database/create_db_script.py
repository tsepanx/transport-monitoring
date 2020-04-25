import peewee as pw

from src.utils.functions import convert

# db = pw.PostgresqlDatabase(db_path)
pg_db = pw.PostgresqlDatabase('transport', user='stepan', password='password', host='95.85.18.95', port=5432)


class BaseModel(pw.Model):
    class Meta:
        database = pg_db

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
    pg_db.create_tables(tables)
