import time
from djitellopy import tello
import KeyPressModule as kp
import cv2
import numpy as np
import math

########### PARAMETERS ################
fSpeed = 117 / 10  # forward speed cm/s
aSpeed = 360 / 10  # angular speed deg/s
interval = 0.25  # time interval in seconds

dInterval = fSpeed * interval  # distance interval
aInterval = aSpeed * interval  # angle interval

########## PARAMETERS #################

global img

kp.init()

drone = tello.Tello()
drone.connect()

print(drone.get_battery())

x, y = 500, 500
ang = 0
yawAng = 0
points = [(0, 0), (0, 0)]

drone.streamon()


def getKeyboardInput():
    lr, fb, up, yaw = 0, 0, 0, 0
    speed = 15
    aSpeed = 50
    dist = 0
    global yawAng, x, y, ang, interval
    if kp.getKey('LEFT'):
        lr = -speed
        dist = dInterval
        ang = -180

    elif kp.getKey('RIGHT'):
        lr = speed
        dist = dInterval
        ang = 0

    if kp.getKey('UP'):
        fb = speed
        dist = dInterval
        ang = 270

    elif kp.getKey('DOWN'):
        fb = -speed
        dist = dInterval
        ang = 90

    if kp.getKey('w'):
        up = speed
    elif kp.getKey('s'):
        up = -speed

    if kp.getKey('d'):
        yaw = aSpeed
        yawAng += aInterval

    elif kp.getKey('a'):
        yaw = -aSpeed
        yawAng -= aInterval

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.1)

    time.sleep(interval)
    ang += yawAng

    print(str(ang))

    x += int(dist * math.cos(math.radians(ang)))
    y += int(dist * math.sin(math.radians(ang)))

    return [lr, fb, up, yaw, x, y]


def drawPoints(img, points):
    for pt in points:
        cv2.circle(img, pt, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

while True:
    if kp.getKey('t'):
       drone.takeoff()
    elif kp.getKey('q'):
        drone.streamoff()
        drone.land()
        break

    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)  # 1000 pixel X 1000 pixels and 3 colors (BGR) values 0 to 255
    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
