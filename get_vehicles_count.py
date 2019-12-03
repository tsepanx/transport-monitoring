from classes import *
from yandex_transport_webdriver_api import *

def write_data_to_file(func, file, url):
      print("---Requesting data---")
      data = func(url)
      with open(file, 'w') as fout:
            fout.write(json.dumps(data, indent=4, separators=(',', ': ')))    

proxy = YandexTransportProxy('127.0.0.1', 25555)

stop_434_id = 10110344
stop_641_id = 9650362

url_641_path = "https://yandex.ru/maps/213/moscow/routes/bus_641/796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393234313135266c6c3d33372e34363738313925324335352e373134333130266e616d653d36343126723d3133323626747970653d627573?ll=37.481413%2C55.714575&z=14"
random = "https://yandex.ru/maps/213/moscow/?ll=37.566902%2C55.799467&masstransit%5BlineId%5D=213_12_bus_mosgortrans&masstransit%5BthreadId%5D=213A_12_bus_mosgortrans&mode=stop&z=12"

file_434_stop = "stop_434.json"
file_641_path = "path_641.json"

write_data_to_file(proxy.get_line, file_641_path, random)

# data = proxy.get_stop_info(get_stop_url(stop_434_id))
# data = proxy.get_line(url_641_path)

# with open('stop_434.json', 'w') as file:
#       file.write(json.dumps(data, indent=4, separators=(',', ': ')))
