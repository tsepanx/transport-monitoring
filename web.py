import os
import sys

from bottle import run, template, static_file, abort, Bottle, debug

from database import RouteData, StopData, Schedule


def filter_table(timetable, exclude_fields=None):
    res = []
    for row in timetable:
        temp = []
        for attr in row:
            if attr[0] not in exclude_fields:
                temp.append(attr)
        res.append(temp)

    return res


app = Bottle()
debug(True)

dirname = os.path.dirname(sys.argv[0])

my_module = os.path.abspath(__file__)
parent_dir = os.path.dirname(my_module)
static_dir = os.path.join(parent_dir, 'static')


@app.route('/<some_pth>/static/:path#.+#', name='static')  # TODO try another code impl.
def static(path, some_pth):
    print(path)
    return static_file(path, root=static_dir)


@app.route('/static/:path#.+#', name='static')
def static(path):
    print(path)
    return static_file(path, root=static_dir)


@app.route('/')
def index():
    return template('index.tpl')


@app.route('/<route_name>')
def route_stops(route_name):
    for row in RouteData.select():
        if row.name == route_name:
            break
    else:
        abort(401, "No such route name in db")

    route_stops = []

    query = StopData.select()
    for route_stop in query:
        if route_stop.route.name == route_name:
            route_stops.append(route_stop)

    return template('route.tpl', route_name=route_name, stops_list=route_stops)


@app.route('/<route_name>/<stop_id>')
def stop_timetable(route_name, stop_id):
    table = Schedule.by_stop_id(route_name, stop_id)
    stop_name = table[0].stop.name_mgt

    res_table = filter_table(table, exclude_fields=['ya_stop', 'stop', 'route', 'name', 'name_mgt'])

    return template('timetable.tpl', route_name=route_name, timetable=res_table, stop_name=stop_name)


if __name__ == '__main__':
    run(app, host='localhost', port=8000)
