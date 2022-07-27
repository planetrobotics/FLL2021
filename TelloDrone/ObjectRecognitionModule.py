import cv2
import cvzone
import numpy as np
import time

class ballDetect:

    def __init__(self): # initializing variables and assinging them to the class
        self.classNames = []
        classFile = 'coco.names'
        with open(classFile, 'rt') as f:
            self.classNames = f.read().split('\n')
        configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'frozen_inference_graph.pb'
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath) # using deeplearning to recognize objects
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)
        self.BALL_CLASSID = 37

    def getBall(self, img):
        #success, img = img.get_frame_read()
        success = True
        img = cv2.flip(img, 1)
        thres = 0.35 # threshold for how confident it has to be in an answer
        nmsThres = 0.2
        if(success): # if it is confident enough in an answer
            classIds, confs, bbox = self.net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
            boxToReturn = []
            try:
                for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    if classId == 37: # only detecting ball
                        cvzone.cornerRect(img, box) # drawing the box around the ball
                        x, y, w, h = box # define box as the x, y, width and height
                        center = x + w/2, y + h/2
                        area = w * h # calculating the box's area
                        boxToReturn = [center, area, w, h] # what it will return
                        #cv2.putText(img, f'{classNames[classId - 1].upper()}{round(conf * 100, 2)}',
                        #            (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
                        #cv2.waitKey(1)
                #        return box
            except:
                pass
        #cv2.imshow("Image", img)
        return img, boxToReturn

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    ball = ballDetect()
    while True:
        success, img = cap.read()
        if success:
            img, box = ball.getBall(img)
            print(str(box))
        cv2.imshow("Image", img)
        cv2.waitKey(1)
