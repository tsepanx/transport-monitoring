import json

"""
Gett
"""

# from YandexTransportWebdriverAPI import YandexTransportProxy
from yandex_transport_webdriver_api import *

if __name__ == '__main__':
      # Route  : Tram "A", Moscow
      # Маршрут: Трамвай "А", Москва
      url = 'https://yandex.ru/maps/213/moscow/?ll=37.670196%2C55.730905&masstransit[lineId]=213_A_tramway_mosgortrans&masstransit[stopId]=stop__9645568&masstransit[threadId]=2036927519&mode=stop&z=13'
      url2 = 'https://yandex.ru/maps/213/moscow/?ll=37.670196%2C55.730905&' \
            'masstransit[lineId]=213_275_bus_mosgortrans&masstransit%5BthreadId%5D=213A_275_bus_mosgortrans&mode=masstransit&z=13'
      url3 = "https://yandex.ru/maps/214/dolgoprudniy/?ll=37.521372%2C55.936159&masstransit%5BrouteId%5D=2037272262&masstransit%5BstopId%5D=stop__9688641&masstransit%5BthreadId%5D=2037281383&mode=stop&z=16"
      url4 = "https://yandex.ru/maps/213/moscow/stops/stop__9647487/?ll=37.743904%2C55.651365&z=18"
      url5 = "https://yandex.ru/maps/213/moscow/routes/bus_158/796d617073626d313a2f2f7472616e7369742f6c696e653f69643d3231335f3135385f6275735f6d6f73676f727472616e73266c6c3d33372e36333338383525324335352e373334393534266e616d653d31353826723d3237303326747970653d627573?ll=37.637834%2C55.735515&z=13"
      url6 = "https://yandex.ru/maps/213/moscow/routes/bus_641/796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393234313135266c6c3d33372e34363738313925324335352e373134333130266e616d653d36343126723d3133323626747970653d627573?ll=37.474185%2C55.714808&z=13"

      print('Counting trams on route "A"...')
      proxy = YandexTransportProxy('127.0.0.1', 25555)
      # a = proxy.get_all_info(url5)
      a = proxy.get_vehicles_info_with_region(url6)
      # vehicles_data = proxy.get_vehicles_info_with_region(url4)
      # vehicles_count = proxy.count_vehicles_on_route(vehicles_data)
      # print(vehicles_data)
      print("--------------")
      print(a)
      with open('data5.json', 'w') as file:
            file.write(json.dumps(a, indent=4, separators=(',', ': ')))
