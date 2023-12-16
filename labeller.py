import cv2
import numpy as np
import math
import os

def clickHandler(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        crosses.append((x,y))

dir = os.fsencode("sample_maps_zipped/map_gif_1km/")

premadef = open("mariaIntersections.txt", "r")
premade = {}
for l in premadef.readlines():
    fx,fy,c = l.split(",")
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
for a, f in enumerate(sorted(os.listdir(dir))):
    if a % 1 != nr:
        continue
    print(f)
    n = f.decode().split(".")[0].split("_")[1:]
    n1, n2 = int(n[0]), int(n[1])
    print(n1, n2)
    if (n1, n2) in lines:
        continue

    p = os.fsdecode(f)
    cap = cv2.VideoCapture("sample_maps_zipped/map_gif_1km/" + p)
    ret, im = cap.read()
    cap.release()

    
    crosses = []
    cv2.namedWindow("i1") 
    cv2.setMouseCallback("i1", clickHandler)
    while 1:
        imn = im.copy()
        for c in crosses:
            imn = cv2.circle(imn, c, 3, (255,0,0), 2)
        cv2.imshow("i1",imn)
        k = cv2.waitKey(1)
        if k == ord(" "):
            break
        elif k == ord("d"):
            crosses = []
        elif k == ord("q"):
            os.exit()

    savef = open("saved", "a")
    savef.write(",".join(str(f).split(".")[0].split("_")[1:]))
    savef.write(",")
    savef.write("|".join([str(c[0])+";"+str(c[0]) for c in crosses]))
    savef.write("\n")
    savef.flush()