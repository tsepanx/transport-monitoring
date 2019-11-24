# Basic example, get stop info and save it to a file

import json
from yandex_transport_webdriver_api import YandexTransportProxy

proxy = YandexTransportProxy('127.0.0.1', 25555)
url = "https://yandex.ru/maps/213/moscow/?ll=37.742975%2C55.651185&masstransit%5BstopId%5D=stop__9647487&mode=stop&z=18"
url2 = "https://yandex.ru/maps/213/moscow/?ll=37.463335%2C55.720286&masstransit%5BstopId%5D=stop__9650362&mode=masstransit&z=18"
data = proxy.get_stop_info(url2)
with open('stop_sources.json', 'w') as file:
    file.write(json.dumps(data, indent = 4, separators = (',', ': ')))
