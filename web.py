from bottle import route, run, template


@route ('/<routeNumber>/<stopId>')
def show_bus_timetable(routeNumber, stopId):
    return template('web.tpl', routeNumber=routeNumber, stopId=stopId)
run(host = 'localhost', port = 8080)



