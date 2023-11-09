import cv2

cap = cv2.VideoCapture("media/map_476000_6546000.gif")
ret, im = cap.read()
cap.release()
print(im)
cv2.imshow("i", im)


im = cv2.inRange(im, cv2.Scalar(0,0,0), cv2.Scala(40,40,40))
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


