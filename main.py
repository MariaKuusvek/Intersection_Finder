import json
import utm
import glob
import cv2
from pyproj import Proj, transform
import numpy as np

def road_convert():
    est97 = Proj(init='epsg:3301')
    wgs84 = Proj(init='epsg:4326')

    file = open("../n_alusdokumendid_ja_lepingud_xgis.geojson", "r")
    data = file.read()
    file.close()
    data = json.loads(data)["features"]
    data = [x["geometry"] for x in data]

    c = 0

    linestrings = []
    multilinestrings = []
    for a in data:
        if a["type"] == "LineString":
            linestrings.append(a["coordinates"])
        else:
            multilinestrings.append(a["coordinates"])
    
    roads = []
    for i, road in enumerate(linestrings):
        new_road = []
        for val in road:
            conv = inv_conv(val[0], val[1], est97, wgs84)
            c += 1
            if c % 100 == 0:
                print(c)
            new_road.append(conv)
            #print(f"{val} -> {conv}")
        roads.append(new_road)
        print(f"Road {i} parsed")
        #break
    
    print("Multiline road start")
    for i, road in enumerate(multilinestrings):
        for subroad in road:
            new_road = []
            for val in subroad:
                conv = inv_conv(val[0], val[1], est97, wgs84)
                c += 1
                if c % 100 == 0:
                    print(c)
                new_road.append(conv)
            roads.append(new_road)
        print(f"Multiroad {i} parsed")
        #break
    file = open("raw_roads2.json", "w")
    file.write(json.dumps(roads))
    file.close()


def road_display():
    file = open("raw_roads.json", "r")
    roads = json.loads(file.read())
    file.close()
    minx = 99999999999999999
    maxx = 0
    miny = 99999999999999999
    maxy = 0
    for road in roads:
        for x, y in road:
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
    xdiff = maxx - minx
    ydiff = maxy - miny
    img = np.zeros([1000,1000,3], dtype=np.uint8)
    img.fill(255)
    for road in roads:
        for x, y in road:
            tx = x - minx
            tx /= xdiff
            tx = int(tx * 1000)
            ty = y - miny
            ty /= ydiff
            ty = int(ty * 1000)
            cv2.circle(img, (tx, 1000 - ty), 1, (0, 0, 255), -1)
    cv2.imshow("i", img)
    cv2.waitKey()
    print(minx, maxx)
    print(miny, maxy)


def main():

    file = open("raw_roads.json", "r")
    roads = json.loads(file.read())
    file.close()
    file = open("raw_roads2.json", "r")
    roads += json.loads(file.read())
    file.close()
    
    for filename in glob.glob("sample_maps_zipped/map_gif_1km/*"):
        coords = filename.split("/")[-1].split(".")[0].split("_")[1:]
        x, y = int(coords[0]), int(coords[1])

        #xl = x
        #x = x - 1000
        xl = x + 1000

        #yl = y
        #y = y - 1000
        yl = y + 1000

        cap = cv2.VideoCapture(filename)
        ret, im = cap.read()
        cap.release()
        #xl, yl = utm.to_latlon(x, y, 35, 'V')

        for i, road in enumerate(roads):
            for val in road:
                if x <= val[0] < xl and y <= val[1] < yl:
                    tx = val[0] - x
                    ty = val[1] - y
                    cv2.circle(im, (int(tx), 1000 - int(ty)), 5, (0, 0, 255), 2)
                    print(val)
        
        print(coords, filename)
        im = cv2.resize(im, (800, 800))
        cv2.imshow("i", im)
        if cv2.waitKey() == 27:
            break
    return

    print(len(linestrings))
    print(len(multilinestrings))
    print(linestrings[0])
    print()
    for a in multilinestrings[0]:
        print(a)

def conv(x, y):
    #x, y = l_est97.x, l_est97.y
    #x = 515000
    #y = 6546000
    est97 = Proj(init='epsg:3301')
    wgs84 = Proj(init='epsg:4326')
    #long, lat = est_97(y, x, inverse=True)
    lon, lat = transform(est97, wgs84, x, y)
    return lon, lat
    #return WGS84(long, lat)

def inv_conv(lon, lat, est97, wgs84):
    x, y = transform(wgs84, est97, lon, lat)
    return x, y


if __name__ == '__main__':
    main()
    #print(conv(515000, 6545000))
    #print(conv(516000, 6546000))
    #road_convert()
    #road_display()
    #conv()
    #print(conv(515000, 6546000))
    #print(inv_conv(24.261392610007295, 59.05256401726076))
