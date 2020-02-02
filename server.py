import threading
import time
from datetime import timedelta, datetime

from constants import *
from database import ArrivalTime, ServerTimeFix
from request import YandexApiRequest, Request
from bottle import route, run, template


class ServerManager:
    def __init__(self, route_name,
                 interval,
                 duration=timedelta(seconds=60)):

        self.interval = interval
        self.made_iterations = 0

        iterations = round(duration.seconds / interval)
        self.main_thread = threading.Thread(target=self.run_async,
                                            args=[iterations], kwargs={'route_name': route_name,
                                                                       'filter': Filter(0, 0)})
        self.main_thread.start()

    def run_async(self, count, **kwargs):
        while self.made_iterations < count:
            value = self.main_request_func(**kwargs)
            ServerTimeFix.create(request_time=datetime.now(), estimated_time=value)

            self.made_iterations += 1
            print(self.made_iterations)
            time.sleep(self.interval)

    def main_request_func(self, route_name='732', filter=Filter(0, 0)):
        stop_request = YandexApiRequest(Request.GET_STOP_INFO, route_name)
        stop_request.run()

        data = stop_request.obtained_data

        stop_name = data[Tags.STOP_NAME]

        estimated_list = data[route_name][Tags.ESTIMATED]
        db_times = list(map(lambda x: x.arrival_time, ArrivalTime.by_stop_name(route_name, stop_name, filter)))

        if len(estimated_list) == 0:
            print("--- No buses on path now ---")
            return None
        #nearest_income = estimated_list[0]
        nearest_income_left = estimated_list[0]
        nearest_income_right = estimated_list[len(estimated_list)-1]

        close_values = {}
        #for i, t in enumerate(db_times):
         #   if t >= nearest_income:
           #     close_values = [db_times[i - 1], t]
            #    break

        for i, t in enumerate(db_times):
            if t >= nearest_income_left and db_times[i-1] < nearest_income_left:
                left_border = i
            if t >= nearest_income_right and db_times[i-1] < nearest_income_right:
                right_border = i
                close_values = db_times[left_border-1 : right_border+1]
                break

        print("real time:", *estimated_list, "times from db:", *close_values, sep="\n")
        #print(self.made_iterations, "request finished")
        print("=====\n")

        # TODO check it resolved completely
        web_info = []

        for i in range (len(estimated_list)):
            d = {}
            d['actual'] = estimated_list[i]
            d['expected'] = close_values[i]
            web_info.append(d)

        #return nearest_income  ###

        @route('/<routeNumber>/<stopId>')
        def show_bus_timetable(routeNumber, stopId):
            return template('web.tpl', routeNumber=routeNumber, stopId=stopId, web_info = web_info)

        run(host='localhost', port=8080)


def main():
    route_name = "732"

    duration = int(input("duration: "))
    interval = int(input("interval: "))

    manager = ServerManager(duration=timedelta(seconds=duration), interval=interval, route_name=route_name)

    while manager.main_thread.is_alive():
        pass


if __name__ == '__main__':
    main()
