import cv2
import io
import numpy as np
import math
import serial
import picamera
import picamera.array
import time

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)           # linux

cap = cv2.VideoCapture(0)
cap.set(3,160)
cap.set(4,120)

while True:
    ret, frame = cap.read ()
    low_b = np.uint8([5,5,5])
    high_b = np.uint8([0,0,0])
    mask = cv2.inRange(frame, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask,1, cv2.CHAIN_APPROX_NONE)[-2:]
    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 120 :
                print("Turn Left")
                ser.write(chr(4).encode())
            if cx < 120 and cx > 40 :
                print("On Track!")
                ser.write(chr(1).encode())
            if cx <=40 :
                print("Turn Right")
                ser.write(chr(3).encode())
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
    else :
        print("I don't see the line")
        ser.write(chr(5).encode())
    cv2.drawContours(frame, c, -1, (0,255,0), 1)
    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
        ser.write(chr(5).encode())
        break
cap.release()
cv2.destroyAllWindows()

