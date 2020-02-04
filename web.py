from bottle import route, run, template


@route('/<route_number>/<stop_id>')
def show_bus_timetable(route_number, stop_id):

    # ------
    # TODO Some logic here
    # ------

    web_info = {}

    return template('web.tpl',
                    route_number=route_number,
                    stop_id=stop_id,
                    web_info=web_info)


def main():
    run(host='localhost', port=8000)


if __name__ == '__main__':
    main()
