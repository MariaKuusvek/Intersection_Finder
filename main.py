import json


def main():
    file = open("riigiteed_xgis.geojson", "r")
    data = file.read()
    file.close()
    data = json.loads(data)["features"]
    data = [x["geometry"] for x in data]
    linestrings = []
    multilinestrings = []
    for a in data:
        if a["type"] == "LineString":
            linestrings.append(a["coordinates"])
        else:
            multilinestrings.append(a["coordinates"])
    print(len(linestrings))
    print(len(multilinestrings))
    print(linestrings[0])
    print()
    for a in multilinestrings[0]:
        print(a)


if __name__ == '__main__':
    main()
