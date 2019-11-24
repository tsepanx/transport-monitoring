#!/usr/bin/env python3

import json

"""
Gett
"""

# from YandexTransportWebdriverAPI import YandexTransportProxy
from yandex_transport_webdriver_api import *

if __name__ == '__main__':
      # Route  : Tram "A", Moscow
      # Маршрут: Трамвай "А", Москва
      url = 'https://yandex.ru/maps/213/moscow/?ll=37.670196%2C55.730905&' \
          'masstransit[lineId]=213_A_tramway_mosgortrans&' \
          'masstransit[stopId]=stop__9645568&' \
          'masstransit[threadId]=2036927519&' \
          'mode=stop&z=13'

      url2 = 'https://yandex.ru/maps/213/moscow/?ll=37.670196%2C55.730905&' \
            'masstransit[lineId]=213_275_bus_mosgortrans&masstransit%5BthreadId%5D=213A_275_bus_mosgortrans&mode=masstransit&z=13'

      url3 = "https://yandex.ru/maps/214/dolgoprudniy/?ll=37.521372%2C55.936159&masstransit%5BrouteId%5D=2037272262&masstransit%5BstopId%5D=stop__9688641&masstransit%5BthreadId%5D=2037281383&mode=stop&z=16"

      print(url)
      print(url2)

      print('Counting trams on route "A"...')
      proxy = YandexTransportProxy('127.0.0.1', 25555)
      a = proxy.get_all_info(url3)
      vehicles_data = proxy.get_vehicles_info_with_region(url3)
      vehicles_count = proxy.count_vehicles_on_route(vehicles_data)
      print(vehicles_data)
      print("--------------")
      print(a)
      with open('data2.json', 'w') as file:
            file.write(json.dumps(vehicles_data,indent=4, separators=(',', ': ')))
