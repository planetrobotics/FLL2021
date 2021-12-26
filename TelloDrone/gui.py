import cv2
from PIL import Image
from PIL import ImageTk
import threading
import tkinter as tk
from djitellopy import Tello
#from ObjectFollowModule import *

drone = Tello()
drone.connect()
print(drone.query_wifi_signal_noise_ratio())

drone.streamoff()

global panel

def button1_clicked():
    thread = threading.Thread(target=videoLoop, args=())
    thread.start()

def button2_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()

def destroy():
    global panel
    drone.streamoff()
    panel.destroy()

def videoLoop(mirror=False):
    global panel
    drone.streamon()

    while True:
        image = drone.get_frame_read().frame
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (800, 600))
        #cv2.imshow("Output", image)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(image=image, compound="top")
        panel.image = image
        panel.place(x=50, y=50)

    return panel


root = tk.Tk()
root.geometry("1920x1080+0+0")

button1 = tk.Button(root, text="start", bg="#fff", font=("",50), command=button1_clicked)
button1.place(x=1000, y=100, width=400, height=250)

button2 = tk.Button(root, text="stop", bg="#fff", font=("",50), command=button2_clicked)
button2.place(x=1000, y=360, width=400, height=250)

root.mainloop()
