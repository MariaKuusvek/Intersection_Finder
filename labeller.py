#!/usr/bin/python
import cv2
import numpy as np
import math
import os
import glob
import json
import sys

import client

conf = json.loads(open("seetings.json","r").read())


hovercoords = (0,0)
def clickHandler(event, x, y, flags, params):
    #if event == cv2.EVENT_LBUTTONDOWN:
    #    crosses.append((x,y))
    global hovercoords
    hovercoords = (x, y)

folder1 = "train_black"
folder2 = "train_map"
folder3 = "train_orto"
basefolder = conf["basefolder"]
folder = folder3

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
amount_done = len(lines)


nr = conf["modulo"]
#print(glob.glob(f"{dir}*.png"))
for a, f in enumerate(sorted(glob.glob(f"{dir}*.png"))):
    if a % 32 != nr:
        continue
    #print(f)
    others = [x.replace(",", ": ") for x in client.send(conf["name"], amount_done).split(";")]
    others = ", ".join(others)
    p = "_".join(f.split(os.path.sep)[-1].split("_")[1:])
    n = p.split(".")[0].split("_")
    n1, n2 = int(n[0]), int(n[1])
    #print(n1, n2)
    if (n1, n2) in lines:
        continue

    #p = os.fsdecode(f)
    print(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
    im = cv2.imread(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
    #cap = cv2.VideoCapture()
    #ret, im = cap.read()
    #cap.release()

    coords = str(f).split(".")[0].split("_")[-2:]
    try:
        crosses = [(int(int(i[0]) * conf["dimx"] / 1000), int(int(i[1]) * conf["dimy"] / 1000)) for i in premade[tuple(coords)]]
    except:
        crosses = []
    cv2.namedWindow("i1") 
    cv2.setMouseCallback("i1", clickHandler)
    clickmode = "add"
    ctr = 0
    while 1:
        imn = im.copy()
        ctr+=1
        imn = cv2.putText(imn, f"{a//32}/{6000//32}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        imn = cv2.putText(imn, others, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        for c in crosses:
            imn = cv2.circle(imn, (int(c[0] / conf['dimx'] * 1000), int(c[1] / conf['dimy'] * 1000)), ((ctr//10)%10)+1, ((ctr*11)%255,(ctr*7)%255,(ctr*3)%255), 2)
        imn = cv2.resize(imn, (conf["dimx"], conf["dimy"]))
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
            if not crosses:
                continue
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
            print(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
            im = cv2.imread(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
        elif k == ord(conf["folder2_key"]):
            folder = folder2
            print(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
            im = cv2.imread(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
        elif k == ord(conf["folder3_key"]):
            folder = folder3
            print(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
            im = cv2.imread(f"{basefolder}{os.path.sep}{folder}{os.path.sep}" + folder.split("_")[1] + "_" + p)
        elif k == ord(conf["back_key"]):
            savef = open("saved","r")
            contents = savef.readlines()[:-1]
            savef.close()
            savef = open("saved", "w")
            savef.write("".join(contents))
            savef.close()
            os.execv(sys.argv[0], sys.argv)

    savef = open("saved", "a")
    savef.write(",".join(",".join(str(f).split(".")[0].split("_")[1:]).split(",")[1:]))
    savef.write(",")
    savef.write("|".join([str(c[0] / conf['dimx'] * 1000)+";"+str(c[1] / conf['dimy'] * 1000) for c in crosses]))
    savef.write("\n")
    savef.close()
    amount_done += 1
