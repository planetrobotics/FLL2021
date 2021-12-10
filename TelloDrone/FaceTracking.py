import time

import cv2
import numpy as np
from djitellopy import tello

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
drone.takeoff()
drone.send_rc_control(0, 0, 15, 0)
time.sleep(2)


# drone.send_rc_control(0, 0, 0, 0)

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + (w // 2)
        cy = y + (h // 2)
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListC) > 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(drone, info, w, pid, pError):
    x, y = info[0]
    area = info[1]

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    fb = 0
    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif fbRange[0] > area > 100:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    # print(speed, fb)

    drone.send_rc_control(0, fb, 0, speed)
    return error


# cap = cv2.VideoCapture(0)
while True:
    # _, img = cap.read()
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(drone, info, w, pid, pError)
    print("Center", info[0], "Area", info[1])
    cv2.imshow("Output", img)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # drone.streamoff()
        drone.land()
        break
