from main import *
import json

def swap(swap_list):
    a = swap_list[0]
    swap_list[0] = swap_list[1]
    swap_list[1] = a

do_request('732', Request.GET_LINE)




with open("line_732.json", "r") as read_file:
    data = json.load(read_file)

features_list = data['data']['features'][0]['features']

coordinates_list = []

for feature in features_list:
    if 'coordinates' in feature:
            swap(feature['coordinates'])
            coordinates_list.append(feature['coordinates'])
    if 'bounds' in feature:
        for bounds in feature['bounds']:
            swap(bounds)
            coordinates_list.append(bounds)
    if 'points' in feature:
        for points in feature['points']:
            swap(points)
            coordinates_list.append(points)

for item in coordinates_list:
    print(item)

res_dict = {}
res_dict["type"] = "Feature"
res_dict["options"] = {"strokeColor": "#b700ff", "strokeWidth": 3}
res_dict["geometry"] = {"type":"LineString", "coordinates": coordinates_list}

with open("polyline.json", "w") as write_file:
    json.dump(res_dict, write_file, indent=4)