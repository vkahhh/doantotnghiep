#!/usr/bin/env python3.4
#OpenCV 3.1.0
import math
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO                    #Import GPIO library
import serial

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)           # linux
#Import time library
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers

TRIG = 17
ECHO = 27
led = 22

# m11=16
# m12=12
# m21=21
# m22=20

GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input
GPIO.setup(led,GPIO.OUT)                  

# GPIO.setup(m11,GPIO.OUT)
# GPIO.setup(m12,GPIO.OUT)
# GPIO.setup(m21,GPIO.OUT)
# GPIO.setup(m22,GPIO.OUT)

GPIO.output(led, 1)

time.sleep(5)

def stop():
    print ("Stop")
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 0)
    # GPIO.output(m21, 0)
    # GPIO.output(m22, 0)
    ser.write(chr(5).encode())

def forward():
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 1)
    # GPIO.output(m21, 1)
    # GPIO.output(m22, 0)
    print ("Forward")
    ser.write(chr(1).encode())

def back():
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 1)
    # GPIO.output(m21, 0)
    # GPIO.output(m22, 1)
    print ("Back")

def left():
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 0)
    # GPIO.output(m21, 1)
    # GPIO.output(m22, 0)
    print ("Left")
    ser.write(chr(4).encode())

def right():
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 1)
    # GPIO.output(m21, 0)
    # GPIO.output(m22, 0)
    print ("Right")
    ser.write(chr(3).encode())

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break

cap.release()
cv2.destroyAllWindows()        

