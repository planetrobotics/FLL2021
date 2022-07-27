from djitellopy import Tello # Tello Control Lib
from pidmath import droneCalculator # import the PID calculator
import cv2 # computer vision
import time

#########################CONNECTION TO DRONE AND DEFINING VARIABLES#####################################################

drone = Tello()
drone.connect()
drone.for_back_velocity = 0
drone.left_right_velocity = 0
drone.up_down_velocity = 0
drone.yaw_velocity = 0
drone.speed = 0

print(drone.get_battery())

drone.streamoff()
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE
centerScreen = [width / 2, height / 2]
area = 12000

pidval = droneCalculator(centerScreen, area)

drone.takeoff() # drone takeoff
drone.streamon() # drone starts camera

cv2.namedWindow("Image") # creating window
cv2.namedWindow("DroneView") # creating window
cv2.resizeWindow("DroneView", width, height)

#########################CONNECTION TO DRONE AND DEFINING VARIABLES#####################################################
while True:

    frame_read = drone.get_frame_read() # get current droen camera frame from the ndarry(numpy)
    img = frame_read.frame # convert that to an actual image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #image colors

    if img is not None: # if it is getting image so that it doesn't error out otherwise
        cv2.imshow("Image", img)
        velocity, img = pidval.getDroneVelocity(img) # PID values
        cv2.imshow("DroneView", img)

    if velocity is not None and len(velocity) == 3:
        LR, ud, fb = velocity # unpacking
        if LR != 0 and ud != 0 and fb != 0:
            print(velocity)
        drone.send_rc_control(0, fb, ud, LR) # sending input to the drone

    if cv2.waitKey(1) & 0xFF == ord('q'): # land if key "q" pressed
        drone.land()
        break

    cv2.waitKey(1) # small pause
