import cv2
import numpy as np
import math
import os

dir = os.fsencode("sample_maps_zipped/map_gif_1km/")
for f in os.listdir(dir):
    p = os.fsdecode(f)
    print(p)
    cap = cv2.VideoCapture("sample_maps_zipped/map_gif_1km/"+p)
    ret, im = cap.read()
    cap.release()

    im = cv2.inRange(im, (0,0,0), tuple([120 for _ in range(3)]))
    cv2.imshow("i1", im)
    #im = cv2.dilate(im,np.ones((3,3)))
    #cv2.imshow("i2", im)
    im = cv2.erode(im,np.ones((3,3)))
    #cv2.imshow("i3", im)
    #cv2.waitKey(0)

    def d(a,b):
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


    whites = set()
    q = set()

    for x in range(im.shape[0]):
        for y in range(im.shape[1]):
            if im[y][x]:
                whites.add((y,x))
                q.add((y,x))

    groups = []
    group_stats = []
    crosss = set()
    im3 = np.zeros_like(im)
    while q:
        start = q.pop()
        q2 = []
        q2.append(start)
        groups.append(set([start]))
        group_stats.append([start[0],start[0],start[1],start[1]])
        objects = [start]
        synonyms = {}
        obj_hist = [[start]]
        start_obj_used = 0
        pix2obj = {start:0}
        im3[start] = 155
        while q2:
            node = q2[0]
            del q2[0]
            #for delta in [[-1,0],[1,0],[0,-1],[0,1]]:
            for delta in [w2 for w in [[[i,j] for i in range(-1,2)] for j in range(-1,2)] for w2 in w]:
                new = (node[0]+delta[0],node[1]+delta[1])
                if new in q and not new==node:
                    q2.append(new)
                    groups[-1].add(new)
                    group_stats[-1] = (min(group_stats[-1][0],new[0]),max(group_stats[-1][1],new[0]),min(group_stats[-1][2],new[1]),max(group_stats[-1][3],new[1]))
                    if d(objects[pix2obj[node]],new) > 20 and not(pix2obj[node] in synonyms and d(objects[synonyms[pix2obj[node]]], new)<21) and not (d(start,new)<50 and not start_obj_used):
                        objects.append(new)
                        obj_hist.append([[new]])
                        pix2obj[new] = len(objects)-1
                        crosss.add(obj_hist[pix2obj[node]][-1])
                        if im3[new] == 0:
                            im3[new] = 255
                    else:
                        if d(objects[pix2obj[node]],new) > 20 and not(pix2obj[node] in synonyms and d(objects[synonyms[pix2obj[node]]], new)<=20) and d(start,new)<50 and not start_obj_used:
                            objects.append(new)
                            obj_hist.append([[new]])
                            pix2obj[new] = len(objects)-1
                            synonyms[pix2obj[node]] = len(objects)-1
                            synonyms[len(objects)-1] = pix2obj[node]
                            start_obj_used = 1
                        else:
                            if d(objects[pix2obj[node]],new)>20:
                                objects[synonyms[pix2obj[node]]] = new
                                pix2obj[new] = synonyms[pix2obj[node]]
                                obj_hist[pix2obj[new]].append(new)
                                if len(obj_hist[pix2obj[new]]) > 50:
                                    del obj_hist[pix2obj[new]][0]
                            else:
                                objects[pix2obj[node]] = new
                                pix2obj[new] = pix2obj[node]
                                obj_hist[pix2obj[node]].append(new)
                                if len(obj_hist[pix2obj[node]]) > 50:
                                    del obj_hist[pix2obj[node]][0]
                        if im3[new] == 0:
                            im3[new] = 50
                    q.remove(new)
                    #cv2.imshow("show",im3)
                    #cv2.waitKey(1)

    print([len(i) for i in groups])
    imn1 = np.zeros_like(im)
    imn2 = np.zeros_like(im)
    for gi in range(len(groups)):
        if len(groups[gi]) < 100 or max(group_stats[gi][1]-group_stats[gi][0], group_stats[gi][3]-group_stats[gi][2]) < 100:
            continue
        for pix in groups[gi]:
            imn1[pix] = 50
            if pix in crosss:
                imn1[pix] = 255
    #imn1 = cv2.dilate(imn1, np.ones((20,20)))
    cv2.imshow("i2", imn1)
    #cv2.imshow("i3", imn2)
    cv2.waitKey(0)