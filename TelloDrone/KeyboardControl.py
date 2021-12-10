import time
from djitellopy import tello
import KeyPressModule as kp
import cv2

global img

kp.init()

drone = tello.Tello()
drone.connect()

print(drone.get_battery())
drone.streamon()

def getKeyboardInput():
    lr, fb, up, yaw = 0, 0 , 0, 0
    speed = 50
    if kp.getKey('LEFT'): lr = -speed
    elif kp.getKey('RIGHT'): lr = speed

    if kp.getKey('UP'): up = speed
    elif kp.getKey('DOWN'): up = -speed

    if kp.getKey('w'): fb = speed
    elif kp.getKey('s'): fb = speed

    if kp.getKey('d'): yaw = speed
    elif kp.getKey('a'): yaw = -speed

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.1)

    return [ lr, fb, up, yaw ]

while True:
    if kp.getKey('t'): drone.takeoff()
    elif kp.getKey('q'):
        drone.streamoff()
        drone.land()
        break

    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)



