import json

f = open("data.json", "r")

s = f.read()
data = json.loads(s)
print(data["data"]["geometries"][0]["coordinates"])