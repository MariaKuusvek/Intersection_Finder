import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
from pyproj import Proj, transform
import os
from pyproj import Geod
import cv2, glob


def main():
    est97 = Proj(init='epsg:3301')
    wgs84 = Proj(init='epsg:4326')
    file_names = glob.glob("sample_maps_zipped/orto_gif_1km/*")
    answerfile = open("mariaIntersections.txt", "w")
    display = False
    for filename in file_names:
        spl = filename.split("/")[-1].split(".")[0].split("_")
        x = int(spl[1]) + 500
        y = int(spl[2]) + 500
        #print(filename, x, y)
        lon, lat = transform(est97, wgs84, x, y)
        #print(lon, lat)
        G = ox.graph_from_point((lat, lon), dist=2500, network_type='all')
        #ox.show()
        #print()
        #print(x, y)
        #print()
        if display:
            cap = cv2.VideoCapture(filename)
            ret, im = cap.read()
            cap.release()
        bx, by = x - 500, y - 500
        nodes = {}
        road_amounts = {}
        for a in G.nodes(data=True):
            lon = a[1]["x"]
            lat = a[1]["y"]
            x, y = transform(wgs84, est97, lon, lat)
            #print(x, y)
            x = x - bx
            y = y - by
            nodes[a[0]] = (x, y)
            road_amounts[a[0]] = 0
        #print()
        for edge in G.edges():
            #print(edge)
            a, b = edge
            road_amounts[a] += 1
            road_amounts[b] += 1
        road_amounts = {key: value // 2 for key, value in road_amounts.items()}
        #print()
        #print(road_amounts)
        ans = []
        for key, value in nodes.items():
            if road_amounts[key] < 2:
                continue
            x, y = value
            if 0 < x < 1000 and 0 < y < 1000:
                ans.append((int(x), 1000 - int(y)))
                if display:
                    cv2.circle(im, (int(x), 1000 - int(y)), 7, (255, 0, 0), -1)
            #print(x, y)
            #print()
        answerfile.write(f"{spl[1]},{spl[2]}," + "|".join([f"{x[0]};{x[1]}" for x in ans]) + "\n")
        if display:
            im = cv2.resize(im, (800, 800))
            cv2.imshow("asd", im)
            fig, ax = ox.plot_graph(G, node_color='orange', node_size=30, node_zorder=2, node_edgecolor='k')
            if cv2.waitKey() == 27:
                break
        #print()
    answerfile.close()
    
#image1_lon_lat = file_names[0].replace("_", " ").replace(".", " ").split(" ")
#image1_lon_lat = (image1_lon_lat[1], image1_lon_lat[2])
#image1_lon_lat[0]

if __name__ == '__main__':
    main()
