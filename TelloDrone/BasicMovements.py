from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()

print(drone.get_battery())

drone.takeoff()
# drone.move_forward(30)
drone.send_rc_control(0, 20, 0, 0)
sleep(2)
drone.send_rc_control(20, 0, 0, 0)
sleep(2)
drone.land()



