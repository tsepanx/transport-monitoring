import json
from yandex_transport_webdriver_api import *

url = "https://yandex.ru/maps/213/moscow/routes/bus_641/796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393234313135266c6c3d33372e34363738313925324335352e373134333130266e616d653d36343126723d3133323626747970653d627573?ll=37.474213%2C55.712793&z=17"

url_stop = "https://yandex.ru/maps/213/moscow/stops/stop__9644876/?ll=37.469947%2C55.709603&z=17"

def get_url(id):
      return "https://yandex.ru/maps/213/moscow/?masstransit[stopId]=stop__" + str(id)

id = int(input())
proxy = YandexTransportProxy('127.0.0.1', 25555)
# a = proxy.get_vehicles_info_with_region(url)
b = proxy.get_stop_info(get_url(id))
print("--------------")
print(b)

with open('stop.json', 'w') as file:
      file.write(json.dumps(b, indent=4, separators=(',', ': ')))
