from main import *
import json
import random


def swap(swap_list):
    a = swap_list[0]
    swap_list[0] = swap_list[1]
    swap_list[1] = a


def generate_random_latency(stop_list):
    latency_list = []
    for i in range(len(stop_list) - 1):
        latency_list.append(random.randint(0, 2))
    return latency_list


def add_green_feature(features):
    feature = {
        "type": "Feature",
        "options": {"strokeColor": "#32CD32", "strokeWidth": 3},
        "geometry": {
            "type": "LineString",
            "coordinates": []
        }
    }
    features.append(feature)


def add_orange_feature(features):
    feature = {
        "type": "Feature",
        "options": {"strokeColor": "#FF8C00", "strokeWidth": 3},
        "geometry": {
            "type": "LineString",
            "coordinates": []
        }
    }
    features.append(feature)


def add_red_feature(features):
    feature = {
        "type": "Feature",
        "options": {"strokeColor": "#FF0000", "strokeWidth": 3},
        "geometry": {
            "type": "LineString",
            "coordinates": []
        }
    }
    features.append(feature)


do_request('732', Request.GET_LINE)

with open("generated_files/line_732.json", "r") as read_file:
    data = json.load(read_file)

features_list = data['data']['features'][0]['features']
points_list = []
stop_coordinates_list = []

for feature in features_list:
    if 'coordinates' in feature:
        swap(feature['coordinates'])
        stop_coordinates_list.append(feature['coordinates'])

    # if 'bounds' in feature:
    #     for bounds in feature['bounds']:
    #         swap(bounds)
    #         points_list.append(bounds)

    if 'points' in feature:
        points = []
        for points_pair in feature['points']:
            swap(points_pair)
            points.append(points_pair)
        points_list.append(points)

for item in points_list:
    print(item)

res_dict = {
    "type": "FeatureCollection",
    "features": [

    ]
}

latency_list = generate_random_latency(stop_coordinates_list)

# print(len(latency_list))
# print(len(points_list))


for i in range(len(latency_list) - 1):
    if latency_list[i] == 0:
        add_green_feature(res_dict["features"])
        res_dict["features"][i]["geometry"]["coordinates"] = points_list[i]
        res_dict["features"][i]["id"] = i

    if latency_list[i] == 1:
        add_orange_feature(res_dict["features"])
        res_dict["features"][i]["geometry"]["coordinates"] = points_list[i]
        res_dict["features"][i]["id"] = i

    if latency_list[i] == 2:
        add_red_feature(res_dict["features"])
        res_dict["features"][i]["geometry"]["coordinates"] = points_list[i]
        res_dict["features"][i]["id"] = i

# for i in range(len(stop_coordinates_list)):
#      stop_feature = {
#         "type": "Feature",
#         "id": i,
#         "geometry": {
#             "type": "Point",
#             "coordinates": stop_coordinates_list[i]
#         }
#     }
#
#      res_dict["features"].append((stop_feature))


with open("generated_files/polyline.json", "w") as write_file:
    json.dump(res_dict, write_file, indent=4)
