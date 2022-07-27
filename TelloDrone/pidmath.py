import cv2
from ObjectRecognitionModule import ballDetect


class droneCalculator:

    def __init__(self, centerScreen, area):  # initialize variables and ty them to the class so they can be accessed within it.
        self.centerScreen = centerScreen  # getting input variables
        self.area = area
        self.ball = ballDetect()  # object for the ball detection
        self.prevErrorX = 0  # PRevious error for the PID math
        self.prevErrorY = 0
        self.prevErrorA = 0
        self.deadZone = 75
        self.deadZoneA = 3000

        self.kpXY = 0.15
        self.kdXY = 0.3
        self.kiXY = 0.001

        self.kpA = 0.001
        self.kdA = 0.003
        self.kiA = 0

    def getDroneVelocity(self, img):  # get the velocity from the PID math function and the error from the ball detection class
        right_left = 0
        up_down = 0
        forward_backward = 0
        try:
            img, box = self.ball.getBall(img)  # unpacking output
            if box is not None and len(box) > 0:  # if it is getting values
                center, Ab, w, h = box  # unpacking values from box
                Xb, Yb = center  # unpacking center to a x and y value
                errorX = self.centerScreen[0] - Xb
                errorY = self.centerScreen[1] - Yb
                errorA = self.area - Ab
                right_left = self.PID(errorX, self.prevErrorX, self.deadZone, self.kpXY, self.kdXY, self.kiXY)
                up_down = self.PID(errorY, self.prevErrorY, self.deadZone, self.kpXY, self.kdXY, self.kiXY)
                forward_backward = self.PID(errorA, self.prevErrorA, self.deadZoneA, self.kpA, self.kdA, self.kiA)

                # saving error values before they are reset
                self.prevErrorX = errorX
                self.prevErrorY = errorY
                self.prevErrorA = errorA
        except:
            pass

        droneMove = [right_left, up_down, forward_backward] # list that values will be saved in
        return droneMove, img

    def PID(self, error, prevError, deadZone, kp, kd, ki):  # basic PID formula
        if abs(error) < deadZone:
            return 0

        proportional = kp * error
        integral = ki * (error + prevError)
        derivative = kd * (error - prevError)

        return round(proportional + integral + derivative)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    xSize = 640
    ySize = 480
    centerScreen = [xSize / 2, ySize / 2]
    area = 12000

    droneCal = droneCalculator(centerScreen, area)

    while True:
        success, img = cap.read()
        if success:
            droneMovement, img = droneCal.getDroneVelocity(img)
            print(droneMovement)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
