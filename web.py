from bottle import route, run, template, static_file, abort

from constants import ROUTES_FIELDS
from main import filter_database


@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


@route('/')
def index():
    return template('index.tpl')


@route('/<route_name>')
def route_timetable(route_name):
    if route_name not in ROUTES_FIELDS:
        abort(401, "Unknown route")

    data = filter_database(route_name)
    print(data)
    return template('timetable.tpl', route_name=route_name, timetable=data)


if __name__ == '__main__':
    run(host='localhost', port=8000)
