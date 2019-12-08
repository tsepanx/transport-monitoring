from classes import *
from yandex_transport_webdriver_api import *

proxy = YandexTransportProxy('127.0.0.1', 25555)

stop_434_id = 10110344
stop_641_id = 9650362

tram_path = "https://yandex.ru/maps/54/yekaterinburg/routes/tramway_18/796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32313037303438383832266c6c3d36302e36303334323825324335362e383431393433266e616d653d313826723d3437343626747970653d7472616d776179?ll=60.663880%2C56.822647&z=12"
path_5 = "https://yandex.ru/maps/19/syktyvkar/?ll=50.790977%2C61.725981&masstransit%5BlineId%5D=3332066175&masstransit%5BthreadId%5D=3332141745&mode=stop&z=15"


url_641_path = "https://yandex.ru/maps/213/moscow/routes/bus_641/796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393234313135266c6c3d33372e34363738313925324335352e373134333130266e616d653d36343126723d3133323626747970653d627573?ll=37.481413%2C55.714575&z=14"

file_434_stop = "stop_434.json"
file_641_path = "path_641.json"

write_data_to_file(proxy.get_all_info, file_641_path, get_stop_url(stop_641_id))