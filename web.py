from bottle import route, run, template, static_file, abort

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


@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


@route('/')
def index():
    return template('index.tpl')


@route('/<route_name>')
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


@route('/<route_name>/stop/<stop_id>')
def stop_timetable(route_name, stop_id):
    table = Schedule.by_stop_id(route_name, stop_id)

    res_table = filter_table(table, exclude_fields=['ya_stop', 'stop', 'route', 'name'])

    return template('timetable.tpl', route_name=route_name, timetable=res_table)


if __name__ == '__main__':
    run(host='localhost', port=8000)
