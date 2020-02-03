from playhouse.migrate import *

my_db = SqliteDatabase('buses.db')
migrator = SqliteMigrator(my_db)

migrate(
#    migrator.add_column('stopdata', 'coordinates', IntegerField(null=True)),
#    migrator.rename_table('routedata', 'buses'),
#    migrator.drop_column('stopdata', 'stop_id'),
#    migrator.drop_column('stopdata', 'way'),
#    migrator.drop_column('stopdata', 'route_name_id'),
#    migrator.rename_table('arrivaltime', 'schedule'),
#    migrator.rename_table('servertimefix', 'arrivaltime'),
#    migrator.drop_column('schedule', 'stop_name'),
#    migrator.rename_column('schedule', 'route_name_id', 'bus_id'),
#    migrator.add_column('stopdata', 'stop_id', IntegerField(null=True)),
#    migrator.drop_column('stopdata', 'stop_id'),
#    migrator.rename_column('schedule', 'way', 'direction'),
    migrator.drop_column('stopdata', 'coordinates'),

    migrator.add_column('stopdata', 'ya_stop_id', ForeignKeyField(YandexStop, null=True)),
    migrator.add_column('stopdata', 'bus_id', ForeignKeyField(Bus, null=True)),
    migrator.add_column('stopdata', 'direction', IntegerField(null=True)),
    migrator.add_column('stopdata', 'waypoint', IntegerField(null=True)),

)
