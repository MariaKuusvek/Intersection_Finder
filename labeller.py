import cv2
import numpy as np
import math
import os
import glob

conf = {
    "next_key": " ",
    "del_key": "d",
    "quit_key": "q",
    "cross_key": "a",
    "del_single_key": "s",
    "folder1_key": "1",
    "folder2_key": "2",
    "folder3_key": "3"
}


hovercoords = (0,0)
def clickHandler(event, x, y, flags, params):
    #if event == cv2.EVENT_LBUTTONDOWN:
    #    crosses.append((x,y))
    global hovercoords
    hovercoords = (x,y)

folder1 = "black_gif_1km"
folder2 = "map_gif_1km"
folder3 = "orto_gif_1km"
basefolder = "sample_maps_zipped"
folder = folder2

dir = f"{basefolder}{os.path.sep}{folder}{os.path.sep}"

premadef = open("mariaIntersections.txt", "r")
premade = {}
for l in premadef.readlines():
    fx,fy,c = l.strip().split(",")
    premade[(fx,fy)] = [i.split(";") for i in c.split("|")]

try:
    done = open("saved", "r")
    lines = done.readlines()
    done.close()
except:
    lines = []
lines = [x.split(",")[:2] for x in lines]
lines = {(int(x[0]), int(x[1])) for x in lines}


nr = 0
for a, f in enumerate(sorted(glob.glob(f"{dir}*.png"))):
    if a % 1 != nr:
        continue
    #print(f)
    p = f.split(os.path.sep)[-1]
    n = p.split(".")[0].split("_")[1:]
    n1, n2 = int(n[0]), int(n[1])
    #print(n1, n2)
    if (n1, n2) in lines:
        continue

    #p = os.fsdecode(f)
    print(f"sample_maps_zipped{os.path.sep}{folder}{os.path.sep}" + p)
    im = cv2.imread(f"sample_maps_zipped{os.path.sep}{folder}{os.path.sep}" + p)
    #cap = cv2.VideoCapture()
    #ret, im = cap.read()
    #cap.release()

    coords = str(f).split(".")[0].split("_")[1:]
    #crosses = [premade[tuple(coords)]]
    crosses = []
    cv2.namedWindow("i1") 
    cv2.setMouseCallback("i1", clickHandler)
    clickmode = "add"
    while 1:
        imn = im.copy()
        for c in crosses:
            imn = cv2.circle(imn, c, 3, (255,0,0), 2)
        cv2.imshow("i1",imn)
        k = cv2.waitKey(1)
        if k == ord(conf["next_key"]):
            break
        elif k == ord(conf["del_key"]):
            crosses = []
        elif k == ord(conf["quit_key"]):
            os.exit()
        elif k == ord(conf["cross_key"]):
            crosses.append(hovercoords)
        elif k == ord(conf["del_single_key"]):
            mind = 1e9
            mino = None
            for ci in range(len(crosses)):
                c = crosses[ci]
                if (d:=abs(c[0]-hovercoords[0])+abs(c[1]-hovercoords[1])) < mind:
                    mind = d
                    mino = ci
            del crosses[mino]
        elif k == ord(conf["folder1_key"]):
            folder = folder1
            im = cv2.imread(f"sample_maps_zipped{os.path.sep}{folder}{os.path.sep}" + p)
        elif k == ord(conf["folder2_key"]):
            folder = folder2
            im = cv2.imread(f"sample_maps_zipped{os.path.sep}{folder}{os.path.sep}" + p)
        elif k == ord(conf["folder3_key"]):
            folder = folder3
            im = cv2.imread(f"sample_maps_zipped{os.path.sep}{folder}{os.path.sep}" + p)

    savef = open("saved", "a")
    savef.write(",".join(str(f).split(".")[0].split("_")[1:]))
    savef.write(",")
    savef.write("|".join([str(c[0])+";"+str(c[0]) for c in crosses]))
    savef.write("\n")
    savef.close()