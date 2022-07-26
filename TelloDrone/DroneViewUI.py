import time
import threading
from tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk

class DroneViewUI:

    def __init__(self, launchCmd):
        root = Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        resolution = str(width) + 'x' + str(height)
        # root.geometry("800x600+0+0")
        root.geometry(resolution)
        # root.attributes("-fullscreen", True)
        root.title("DroneView Driver Assist")
        self.width = width

        self.root = root

        # Add image file
        bg = ImageTk.PhotoImage(Image.open('Resources/background.png').resize((width, height)))

        # Show image using label
        label1 = Label(root, image=bg)
        label1.place(x=0, y=0)



        self.batteryImage = {
            100 : ImageTk.PhotoImage(Image.open('Resources/battery_full.png').resize((40, 24))),
            75 : ImageTk.PhotoImage(Image.open('Resources/battery_75.png').resize((40, 24))),
            50 : ImageTk.PhotoImage(Image.open('Resources/battery_50.png').resize((40, 24))),
            25: ImageTk.PhotoImage(Image.open('Resources/battery_25.png').resize((40, 24)))
        }




        self.wifiImage = {
            "OK" : ImageTk.PhotoImage(Image.open('Resources/wifi.png').resize((32, 32))),
            "KO" : ImageTk.PhotoImage(Image.open('Resources/no_wifi.png').resize((32, 32)))
        }

        self.launchImage = {
            "launch": ImageTk.PhotoImage(Image.open('Resources/launch.png').resize((76, 50))),
            "land": ImageTk.PhotoImage(Image.open('Resources/land.png').resize((64, 46)))

        }

        self.driverAssistImage = {
            "start": ImageTk.PhotoImage(Image.open('Resources/driverassist.png').resize((299, 128))),
            "stop": ImageTk.PhotoImage(Image.open('Resources/driverassist.png').resize((256, 128)))
        }

        self.forward_back = 0
        self.up_down = 0
        self.right_left = 0

        self.launchCmd = launchCmd
        self.launched = False
        self.running = True

        upImage = ImageTk.PhotoImage(Image.open('Resources/up.png').resize((72, 65)))
        upButton = Button(root, image=upImage, borderwidth=0)
        upButton.place(x=843, y=108)
        upButton.bind("<ButtonPress>", self.up_clicked)
        upButton.bind("<ButtonRelease>", self.up_release)

        downImage = ImageTk.PhotoImage(Image.open('Resources/down.png').resize((68, 58)))
        downButton = Button(self.root, image=downImage, borderwidth=0)
        downButton.place(x=843, y=248)
        downButton.bind("<ButtonPress>", self.down_clicked)
        downButton.bind("<ButtonRelease>", self.down_release)

        rightImage = ImageTk.PhotoImage(Image.open('Resources/right.png').resize((64, 58)))
        rightButton = Button(self.root, image=rightImage, borderwidth=0)
        rightButton.place(x=930, y=180)
        rightButton.bind("<ButtonPress>", self.right_clicked)
        rightButton.bind("<ButtonRelease>", self.right_release)

        leftImage = ImageTk.PhotoImage(Image.open('Resources/left.png').resize((62, 58)))
        leftButton = Button(self.root, image=leftImage, borderwidth=0)
        leftButton.place(x=765, y=180)
        leftButton.bind("<ButtonPress>", self.left_clicked)
        leftButton.bind("<ButtonRelease>", self.left_release)

        forwardImage = ImageTk.PhotoImage(Image.open('Resources/forward.png').resize((60, 70)))
        forwardButton = Button(self.root, image=forwardImage, borderwidth=0)
        forwardButton.place(x=700, y=105)
        forwardButton.bind("<ButtonPress>", self.forward_clicked)
        forwardButton.bind("<ButtonRelease>", self.forward_release)

        reverseImage = ImageTk.PhotoImage(Image.open('Resources/backward.png').resize((60, 80)))
        reverseButton = Button(self.root, image=reverseImage, borderwidth=0)
        reverseButton.place(x=700, y=250)
        reverseButton.bind("<ButtonPress>", self.back_clicked)
        reverseButton.bind("<ButtonRelease>", self.back_release)

        self.launchText = "launch"
        self.launchBtn = Button(self.root, image=self.launchImage[self.launchText], borderwidth=0, command=self.launch)
        self.launchBtn.place(x=840, y=185)

        self.panel = Label(self.root, image=None, compound="top")
        self.panel.image = self.batteryImage[50]
        self.panel.place(x=0, y=5)

        self.assistButton = Button(self.root, image=self.driverAssistImage["start"], borderwidth=0)
        self.assistButton.place(x=718, y=360)

        def openNewWindow():
            # Toplevel object which will
            # be treated as a new window
            newWindow = Toplevel(root)

            # sets the title of the
            # Toplevel widget
            newWindow.title("Help")

            # sets the geometry of toplevel
            newWindow.geometry("500x200")

            # A Label widget to show in toplevel
            Label(newWindow,
                  text="" "\nThere are 2 ways to use DroneView:"
                       "\n\n-Press the manual control buttons to manually move the drone\n \n - Press Driver Assist to make the drone automatically follow the truck\n\n ").pack()




        infoImage = Image.open('Resources/info.png')
        infoImage = infoImage.resize((32, 32))
        infoImage = ImageTk.PhotoImage(infoImage)
        info = Button(self.root, image=infoImage, compound="top",command=openNewWindow)
        info.place(x=(width -75), y=5)





        self.wifi = Label(self.root, image=self.wifiImage["OK"], compound="top")
        self.wifi.place(x=(width - 115), y=5)

        self.battery = Label(self.root, image=self.batteryImage[100], compound="top")
        self.battery.place(x=(width - 165), y=5)
        self.batteryLevel = 100;

        self.launchThread = None

        root.protocol("WM_DELETE_WINDOW", self.onClose)
        root.mainloop()


    def getDroneCommand(self):
        return self.forward_back, self.up_down, self.right_left

    def forward_clicked(self, event):
        self.forward_back = 20

    def forward_release(self, event):
        self.forward_back = 0

    def back_clicked(self, event):
        self.forward_back = -20

    def back_release(self, event):
        self.forward_back = 0

    def up_clicked(self, event):
        self.up_down = 20

    def up_release(self, event):
        self.up_down = 0

    def down_clicked(self, event):
        self.up_down = -20

    def down_release(self, event):
        self.up_down = 0

    def left_clicked(self, event):
        self.right_left = -20

    def left_release(self, event):
        self.right_left = 0

    def right_clicked(self, event):
        self.right_left = 20

    def right_release(self, event):
        self.right_left = 0

    def setLaunched(self, launched):
        self.launched = launched
        self.updateLaunchButton()

    def launch(self):
        th = self.launchCmd(self)
        if th != None:
            self.launchThread = th
        if self.launched:
            self.launched = False
        else:
            self.launched = True
        self.updateLaunchButton()

    def isRunning(self):
        return self.running

    def updateLaunchButton(self):
        if True == self.launched:
            print("launch clicked")
            self.launchBtn.destroy()
            self.launchText = "land"
            self.launchBtn = Button(self.root, image=self.launchImage[self.launchText], borderwidth=0,
                                    command=self.launch)
            self.launchBtn.place(x=845, y=188)

        else:
            self.launchBtn.destroy()
            self.launchText = "launch"
            self.launchBtn = Button(self.root, image=self.launchImage[self.launchText], borderwidth=0,
                                    command=self.launch)
            self.launchBtn.place(x=840, y=185)

    def showCameraFeed(self, image):
        self.panel = Label(self.root, image=image, compound="top")
        self.panel.image = image
        self.panel.place(x=0, y=5)
        time.sleep(0.1)

    def onClose(self):
        self.panel.destroy()
        self.running = False
        self.root.destroy()
        print("UI closed")

    def setBattery(self, batteryLevel):

        level = 100 #default
        if batteryLevel > 85:
            level = 100
        elif batteryLevel > 70:
            level = 75
        elif batteryLevel > 40:
            level = 50
        else:
            level = 25

        if self.batteryLevel != level:
            self.batteryLevel = level
            if self.battery != None:
                self.battery.destroy()
            self.battery = Label(self.root, image=self.batteryImage[level], compound="top")
            self.battery.place(x=(self.width - 165), y=5)

    def setWifi(self, wifiLevel):
        if self.wifi != None:
            self.wifi.destroy()

        wifiAvailable = "OK"
        if False == wifiLevel:
            wifiAvailable = "KO"

        self.wifi = Label(self.root, image=self.wifiImage[wifiAvailable], compound="top")
        self.wifi.place(x=(self.width - 115), y=5)


if __name__ == '__main__':

    launched = False
    battery = 100
    wifi = True

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
        droneUI = DroneViewUI(launchCmd)
    except:
        pass



