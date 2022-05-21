#!/usr/bin/env python3.4
#OpenCV 3.1.0
import math
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO                    #Import GPIO library

#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers

TRIG = 17
ECHO = 27
led = 22

m11=16
m12=12
m21=21
m22=20

GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input
GPIO.setup(led,GPIO.OUT)                  

GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

#GPIO.output(led, 1)

time.sleep(5)

def stop():
    print ("Stop")
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print ("Forward")

def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print ("Back")

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print ("Left")

def right():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print ("Right")

def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope
    m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation
    theta1 = math.atan(m)                  #calculate the slope angle
    return theta1*(180/np.pi)              #Calculated angle in radians


cap = cv2.VideoCapture(0)


a=b=c=1

while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img,(600,600))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(equ,(5,5),0)
    ret, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY)

    # Find Contours
    ret, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw Contour
    cv2.drawContours(thresh, contours, -1, (255, 0, 0), 3)
    
    drawing = np.zeros(img.shape, np.uint8)

    lines = cv2.HoughLinesP(thresh, cv2.HOUGH_PROBABILISTIC, np.pi/180, 25, minLineLength = 10, maxLineGap = 40)
    
    l=r=0
    for line in lines:
        
        for x1,y1,x2,y2 in line:
             if (round(x2-x1)!=0):
                  arctan = slope(x1,x2,y1,y2)
                  
                  if(y1>250 and y1<600 and y2>250 and y2<600):

                       if (round(arctan>=round(-80)) and round(arctan<=round(-30))):
                            r+=1
                            l=0
                            cv2.line(img,(x1, y1),(x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
                  
                       if ( round(arctan>=round(30)) and round(arctan<=round(80))):
                            l+=1
                            r=0
                            cv2.line(img,(x1, y1),(x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
        
                  

    
    if l>=10 and a==1:
        
        print ("Left")

        #time.sleep(0.3)
        a=0
        b=1
        c=1
        left()
    elif r>=10 and b==1:
        print ("Right")
        #time.sleep(0.3)
        a=1
        b=0
        c=1
        right()
    elif l<10 and r<10 and c==1:
        print ("Straight")
        a=1
        b=1
        c=0
        forward()
    cv2.imshow('video', thresh)
    cv2.imshow('video1', img)
    #cv2.imshow('equ', drawing)
    #cv2.imshow('edge', equ)

###### Traffic_light_detection #####
    _, img1 = cap.read()
    #img=img1[10:400,200:400] #for rightmost ROI
    img=img1[30:2000,500:700] #for leftmost ROI

    #img = cv2.resize(img1,(600,600))   
    #converting frame(img i.e BGR) to HSV (hue-saturation-value)

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #definig the range of red color
    red_lower=np.array([136,87,111],np.uint8)
    red_upper=np.array([180,255,255],np.uint8)


    #defining the Range of green color
    green_lower=np.array([66, 122, 129],np.uint8)
    green_upper=np.array([86,255,255],np.uint8)

    #finding the range of red,green color in the image
    red=cv2.inRange(hsv, red_lower, red_upper)
    green=cv2.inRange(hsv,green_lower,green_upper)

    #Morphological transformation, Dilation  
    kernal = np.ones((5 ,5), "uint8")
    red=cv2.dilate(red, kernal)
    res=cv2.bitwise_and(img, img, mask = red)

    green=cv2.dilate(green,kernal)
    res2=cv2.bitwise_and(img, img, mask = green)    


    #Tracking the Red Color
    (contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>300):

            x,y,w,h = cv2.boundingRect(contour)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            print("Red")
            #time.sleep(1)
            #print('stop')
            stop()

    #Tracking the green Color
    (contours,hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(img,"Green  color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))  
            print("Green")
                #time.sleep(1)
            print("Forward")
            forward()

#### Obstacle detection ###
    count =0
    i=0
    avgDistance=0
    for i in range(5):
      GPIO.output(TRIG, False)                 #Set TRIG as LOW
      time.sleep(0.1)                                   #Delay

    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                           #Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                 #Set TRIG as LOW

    while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
       GPIO.output(led, False)             
    pulse_start = time.time()

    while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
       GPIO.output(led, False) 
    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
    distance = round(distance,2)                 #Round to two decimal points
    avgDistance=avgDistance+distance

    avgDistance=avgDistance/5
    print (avgDistance)
    flag=0
    if avgDistance < 25:
    #Check whether the distance is within 25 cm range
        count=count+1
        stop()
        time.sleep(1)
        #back()
        time.sleep(1.5)
        if (count%3 ==1) & (flag==0):
            right()
            flag=1
        else:
            left()
            flag=0
        time.sleep(1.5)
        stop()
        time.sleep(1)
    else:
        forward()
        flag=0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break

cap.release()
cv2.destroyAllWindows()        

