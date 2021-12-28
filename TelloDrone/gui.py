import time
import cv2
from PIL import Image
from PIL import ImageTk
import threading
import tkinter as tk
from djitellopy import Tello

launched = False

drone = Tello()
drone.connect()
print(drone.query_wifi_signal_noise_ratio())

drone.streamoff()

global panel
global launched

def Left_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()
    print("left clicked")


def Right_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()
    print("right clicked")


def Down_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()
    print("down clicked")


def Up_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()
    print("up clicked")


def Forward_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()
    print("forward clicked")


def Back_clicked():
    thread = threading.Thread(target=destroy, args=())
    thread.start()
    print("back clicked")


def Launch():
    if False == launched:

        thread = threading.Thread(target=videoLoop, args=())
        thread.start()
        print("launch clicked")


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
    drone.streamon()
    image = createImage()
    panel = tk.Label(image=image, compound="top")
    panel.place(x=0, y=5)

    while True:
        img = createImage()
        panel = tk.Label(image=img, compound="top")
        panel.image = img
        panel.place(x=0, y=5)
        time.sleep(0.1)


root = tk.Tk()
root.geometry("800x600+0+0")

button1 = tk.Button(root, text="left", bg="#fff", font=("", 10), command=Left_clicked)
button1.place(x=775, y=175, width=50, height=50)

button2 = tk.Button(root, text="right", bg="#fff", font=("", 10), command=Right_clicked)
button2.place(x=925, y=175, width=50, height=50)

button3 = tk.Button(root, text="down", bg="#fff", font=("", 10), command=Down_clicked)
button3.place(x=850, y=250, width=50, height=50)

button4 = tk.Button(root, text="up", bg="#fff", font=("", 10), command=Up_clicked)
button4.place(x=850, y=105, width=50, height=50)

button5 = tk.Button(root, text="launch", bg="#fff", font=("", 10), command=Launch)
button5.place(x=850, y=175, width=50, height=50)

button6 = tk.Button(root, text="forward", bg="#fff", font=("", 10), command=Forward_clicked)
button6.place(x=725, y=105, width=50, height=50)

button7 = tk.Button(root, text="back", bg="#fff", font=("", 10), command=Back_clicked)
button7.place(x=725, y=250, width=50, height=50)

root.mainloop()


