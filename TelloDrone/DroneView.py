import time
import cv2
import threading
from djitellopy import Tello
from DroneViewUI import DroneViewUI
from PIL import Image
from PIL import ImageTk

if __name__ == '__main__':

    launched = False
    drone = Tello()
    drone.connect()
    drone.streamoff()
    drone.streamon()

    connected = True
    wifi = True
    droneThread = False
    battery = 100

    def connectDrone(firstTime):
        global drone
        global connected
        global wifi
        while False == connected:
            try:
                drone.streamoff()
                drone.streamon()
                wifiSignal = drone.query_wifi_signal_noise_ratio()
                print(wifiSignal)
                wifi = True
                battery = drone.get_battery()
                connected = True
            except:
                wifi = False
                try:
                    wifiSignal = drone.query_wifi_signal_noise_ratio()
                    if wifiSignal > 10: wifi = True
                    battery = drone.get_battery()
                    connected = True
                except:
                    wifi = False

    def droneLaunchCmd(droneUI):
        global launched
        global battery
        global wifi
        global connected
        global droneThread
        global drone
        launchThread = None
        if False == connected:
            droneUI.setWifi(wifi)
            droneUI.setBattery(0)
            connectDrone(False)
            droneUI.setWifi(wifi)
            droneUI.setBattery(battery)
        elif False == launched:
            drone.takeoff()
            droneUI.setLaunched(True)
            if False == droneThread:
                launchThread = threading.Thread(target=droneVideo, args=(droneUI, True))
                launchThread.start()
                droneThread = True
            launched = True
        else: # land
            launched = False
            drone.land()
            droneUI.setLaunched(False)

        return launchThread

    def droneVideo(droneUI, test):
        global drone
        global connected
        global wifi
        droneUI.setWifi(wifi)
        while droneUI.isRunning() == True:
            if False == connected:
                connectDrone(False)
                droneUI.setWifi(wifi)
                drone.takeoff()
                droneUI.setLaunched(True)
            else:
                try:
                    battery = drone.get_battery()
                    droneUI.setBattery(battery)
                    droneUI.setWifi(wifi)
                    # drone.send_keepalive()
                    if battery < 40:
                        print("Battery too low... change battery")
                    elif False == wifi:
                        print("Drone wifi not connected ...")
                    else:
                        try:
                            image = drone.get_frame_read().frame
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            image = cv2.resize(image, (720, 480))
                            image = Image.fromarray(image)
                            img = ImageTk.PhotoImage(image)
                            image.close()
                            droneUI.showCameraFeed(img)
                        except:
                            print("Not able to get image from drone camera, will retry again...")
                            pass

                        forward_back, up_down, right_left = droneUI.getDroneCommand()
                        drone.send_rc_control(0, forward_back, up_down, right_left)
                except:
                    connected = False
                    wifi = False
                    droneUI.setWifi(False)
                    droneUI.setLaunched(False)
                    continue
        print("stopping video")


    # videoLoop for normal webcam
    def videoLoop(droneUI, cap):
        while droneUI.isRunning() == True:
            success, img = cap.read()
            if success:
                image = Image.fromarray(img)
                img = ImageTk.PhotoImage(image)
                droneUI.showCameraFeed(img)
            cv2.waitKey(1)

        print("stopping video")
        cv2.destroyAllWindows()

    # launch for normal webcam
    def launchCmd(droneUI):
        global launched
        global battery
        global wifi
        if False == launched:
            cap = cv2.VideoCapture(0)
            cap.set(3, 720)
            cap.set(4, 480)
            launchThread = threading.Thread(target=videoLoop, args=(droneUI, cap))
            launchThread.start()
            launched = True
            return launchThread
        else:
            battery = battery - 20
            droneUI.setBattery(battery)
            if wifi:
                wifi = False
            else:
                wifi = True
            droneUI.setWifi(wifi)
        return None

    try:
        # droneUI = DroneViewUI(launchCmd)
        droneUI = DroneViewUI(droneLaunchCmd)
    except:
        pass

