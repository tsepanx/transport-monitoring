from bottle import route, run, template


@route('/<route_number>')
def route_timetable(route_number):
    return template('timetable.tpl', route_number=route_number)


def main():
    run(host='localhost', port=8000)


if __name__ == '__main__':
    main()
