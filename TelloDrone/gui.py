import time
import cv2
from PIL import Image
from PIL import ImageTk
import threading
import tkinter as tk
from djitellopy import Tello

drone = Tello()
drone.connect()
print(drone.query_wifi_signal_noise_ratio())

drone.streamoff()

global panel
global launched
global left_right
global up_down
global forward_back
global launchText
global launchBtn

launched = False
left_right = 0
up_down = 0
forward_back = 0
launchText = "Launch"

def Left_clicked(event):
    global left_right
    left_right = -20
    print("left clicked")

def Left_release(event):
    global left_right
    left_right = 0
    print("left released")


def Right_clicked(event):
    global left_right
    left_right = 20
    print("right clicked")

def Right_release(event):
    global left_right
    left_right = 0
    print("right release")


def Down_clicked(event):
    global up_down
    up_down = -20
    print("down clicked")

def Down_release(event):
    global up_down
    up_down = 0
    print("down release")


def Up_clicked(event):
    global up_down
    up_down = 20
    print("up clicked")

def Up_release(event):
    global up_down
    up_down = 0
    print("up release")


def Forward_release(event):
    global forward_back
    forward_back = 0
    print("forward release")

def Forward_clicked(event):
    global forward_back
    forward_back = 20
    print("forward clicked")


def Back_clicked(event):
    global forward_back
    forward_back = -20
    print("back clicked")

def Back_release(event):
    global forward_back
    forward_back = 0
    print("back release")


def Launch():
    global launched
    global launchText
    global launchBtn
    if False == launched:
        drone.takeoff()
        launched = True
        #moveDroneThread = threading.Thread(target=moveDrone, args=())
        #moveDroneThread.start()
        thread = threading.Thread(target=videoLoop, args=())
        #thread.setDaemon()
        thread.start()
        print("launch clicked")
        launchText = "Land"
        launchBtn = tk.Button(root, text=launchText, bg="#fff", font=("", 10), command=Launch)
        launchBtn.place(x=850, y=175, width=50, height=50)
    else:
        print("landing drone")
        drone.streamoff()
        drone.land()
        launched = False
        launchText = "Launch"
        launchBtn = tk.Button(root, text=launchText, bg="#fff", font=("", 10), command=Launch)
        launchBtn.place(x=850, y=175, width=50, height=50)

def destroy():
    global panel
    drone.streamoff()
    panel.destroy()


def createImage():
    image = drone.get_frame_read().frame
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (720, 480))
    ###cv2.imshow("Output", image)
    image = Image.fromarray(image)
    img = ImageTk.PhotoImage(image)
    image.close()
    return img

def videoLoop(mirror=False):
    global panel
    global forward_back
    global up_down
    global left_right
    drone.streamon()
    image = createImage()
    panel = tk.Label(image=image, compound="top")
    panel.place(x=0, y=5)

    while True:
        drone.send_rc_control(0, forward_back, up_down, left_right)
        img = createImage()
        panel = tk.Label(image=img, compound="top")
        panel.image = img
        panel.place(x=0, y=5)
        time.sleep(0.1)


root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
resolution = str(width) + 'x' + str(height)
#root.geometry("800x600+0+0")
root.geometry(resolution)
#root.attributes("-fullscreen", True)

leftBtn = tk.Button(root, text="left", bg="#fff", font=("", 10))
leftBtn.place(x=775, y=175, width=50, height=50)
leftBtn.bind("<ButtonPress>", Left_clicked)
leftBtn.bind("<ButtonRelease>", Left_release)

rightBtn = tk.Button(root, text="right", bg="#fff", font=("", 10))
rightBtn.place(x=925, y=175, width=50, height=50)
rightBtn.bind("<ButtonPress>", Right_clicked)
rightBtn.bind("<ButtonRelease>", Right_release)

downBtn = tk.Button(root, text="down", bg="#fff", font=("", 10))
downBtn.place(x=850, y=250, width=50, height=50)
downBtn.bind("<ButtonPress>", Down_clicked)
downBtn.bind("<ButtonRelease>", Down_release)

upBtn = tk.Button(root, text="up", bg="#fff", font=("", 10))
upBtn.place(x=850, y=105, width=50, height=50)
upBtn.bind("<ButtonPress>", Up_clicked)
upBtn.bind("<ButtonRelease>", Up_release)

launchBtn = tk.Button(root, text=launchText, bg="#fff", font=("", 10), command=Launch)
launchBtn.place(x=850, y=175, width=50, height=50)

forwardBtn = tk.Button(root, text="forward", bg="#fff", font=("", 10))
forwardBtn.place(x=725, y=105, width=50, height=50)
forwardBtn.bind("<ButtonPress>", Forward_clicked)
forwardBtn.bind("<ButtonRelease>", Forward_release)

backBtn = tk.Button(root, text="back", bg="#fff", font=("", 10))
backBtn.place(x=725, y=250, width=50, height=50)
backBtn.bind("<ButtonPress>", Back_clicked)
backBtn.bind("<ButtonRelease>", Back_release)

root.title("DroneView Driver Assist")

root.mainloop()


