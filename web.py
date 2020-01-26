from bottle import route, run, template
from peewee import *


mysql_db = MySQLDatabase('buses.db')


d = {}
while(True):
    t = input()
    if t == 'stop': break
    f = input()
    d[t] = f

@route ('/<routeNumber>/<stopId>')
def show_bus_timetable(routeNumber, stopId):

    res = '<h1>Bus number is ' + routeNumber + ' and stop id is ' + stopId + '</h1>' + '' \
        '<table border = "100" bgcolor = "#F0F0F0" bordercolor = "green"> ' \
        '<tr><td> <h4>estimated time</h4> </td> <td> <h4> db time </h4> </td> </tr>'

    for key in d:
        res += ('<tr><td> ' + str(key) + '</td><td> ' + str(d[key]) + '</td></tr>')
    res += '</table>'
    return res
run(host = 'localhost', port = 8080)



