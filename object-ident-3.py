import cv2
import pygame
import time
from gpiozero import AngularServo
servo =AngularServo(18, initial_angle=0, min_pulse_width=0.0006, max_pulse_width=0.0023)

#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/pi/Desktop/SY23_Science_Fair/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, filename, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects: 
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    pygame.mixer.init()
                    pygame.mixer.music.load(filename)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        continue


    
    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    
    
    while True:
        success, img = cap.read()
        
        result, objectInfo = getObjects(img,0.45,0.2, "cup.mp3", objects=['cup','bottle', 'hat', 'handbag', 'tie', 'kite','plate', 'spoon', 'fork', 'knife', 'bowl', 'cell phone', 'laptop'])
        
        
                                                                                                
        
        
        #
        
        
        
        #print(objectInfo)
        
        
        
        cv2.imshow("Output",img)
        cv2.waitKey(1)
        
        
        
   
        
        #print(objectInfo)
        
        
        
      
    