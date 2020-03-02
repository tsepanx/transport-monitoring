from constants import does_exist, PROJECT_PREFIX
from database import QueryRecord

import peewee as pw

db_path = PROJECT_PREFIX + 'transport'
db = pw.PostgresqlDatabase(db_path)
tables = [QueryRecord]

if not does_exist(db_path):
    db.create_tables(tables)
