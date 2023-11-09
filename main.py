import json
import utm
import glob
import cv2


def main():
    file = open("../riigiteed_xgis.geojson", "r")
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
    
    for filename in glob.glob("sample_maps_zipped/map_gif_1km/*"):
        coords = filename.split("/")[-1].split(".")[0].split("_")[1:]
        x, y = int(coords[0]), int(coords[1])
        cap = cv2.VideoCapture(filename)
        ret, im = cap.read()
        cap.release()
        cv2.imshow("i", im)
        xl, yl = utm.to_latlon(x, y, 35, 'V')
        
        print(coords, filename, xl, yl)
        if cv2.waitKey() == 27:
            break
    return

    print(len(linestrings))
    print(len(multilinestrings))
    print(linestrings[0])
    print()
    for a in multilinestrings[0]:
        print(a)


if __name__ == '__main__':
    main()
