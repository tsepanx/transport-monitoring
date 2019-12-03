from classes import *
from yandex_transport_webdriver_api import *

stop_434_id = 10110344
home_stop_id = 9650362

proxy = YandexTransportProxy('127.0.0.1', 25555)
data = proxy.get_stop_info(get_stop_url(home_stop_id))
print("---Data request completed---")

with open('stop_641.json', 'w') as file:
      file.write(json.dumps(data, indent=4, separators=(',', ': ')))
