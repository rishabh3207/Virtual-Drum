import cv2
import numpy as np
from playsound import playsound

tom2Coords = (50, 450, 350, 650)
tom1Coords = (375, 500, 675, 700)
snareCoords = (700, 500, 1000, 700)
hihatCoords = (900, 200, 1250, 400)

cap = cv2.VideoCapture(0)
cap.set(3,2000)
cap.set(4,1000)
font = cv2.FONT_HERSHEY_COMPLEX
prev = -1
flag = 0
while True:
    _,frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (5,5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 155, 135])
    upper_red = np.array([255, 255, 255])
##    lower=np.array([0,20,150]) #HSV ranges for skin color
##    upper=np.array([20,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            cv2.drawContours(frame, contour, -1, (0,255,0), 3)
            M = cv2.moments(contour)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.putText(frame, "Position of stick\n" + str(cx) + " , " + str(cy), (cx,cy), font, 0.5, (0,255,255))
            flag = 0
            if cx > 50 and cx < 350 and cy > 350 and cy < 650 :
                flag = 1
            if cx > 375 and cx < 675 and cy > 500 and cy < 700 :
                flag = 1
            if cx > 700 and cx < 1000 and cy > 500 and cy < 700 :
                flag = 1
            if cx > 900 and cx < 1250 and cy > 200 and cy < 400 :
                flag = 1
            if flag == 1:
                if prev != 1 and cx > 50 and cx < 350 and cy > 350 and cy < 650 :
                    playsound("1.mp3")
                    prev = 1
                if prev != 2 and cx > 375 and cx < 675 and cy > 500 and cy < 700 :
                    playsound("2.mp3")
                    prev = 2
                if prev != 3 and cx > 700 and cx < 1000 and cy > 500 and cy < 700 :
                    playsound("3.mp3")
                    prev = 3
                if prev != 4 and cx > 900 and cx < 1250 and cy > 200 and cy < 400 :
                    playsound("4.mp3")
                    prev = 4
            else:
                prev = -1

    r1 = cv2.rectangle(frame, (tom1Coords[0], tom1Coords[1]),
                             (tom1Coords[2], tom1Coords[3]), (255, 0, 0), 10)

    r2 = cv2.rectangle(frame, (tom2Coords[0], tom2Coords[1]),
                             (tom2Coords[2], tom2Coords[3]), (0, 255, 0), 10)

    r3 = cv2.rectangle(frame, (snareCoords[0], snareCoords[1]),
                             (snareCoords[2], snareCoords[3]), (0, 0, 255), 10)

    r4 = cv2.rectangle(frame, (hihatCoords[0], hihatCoords[1]),
                             (hihatCoords[2], hihatCoords[3]), (125, 125, 0), 10)
    cv2.imshow("Virtual Drum",r1)
    cv2.imshow("Virtual Drum",r2)
    cv2.imshow("Virtual Drum",r3)
    cv2.imshow("Virtual Drum",r4)
    cv2.imshow("Virtual Drum", frame)
    cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(1)
    if key == 27 or key == 113:
        break
cap.release()
cv2.destroyAllWindows()
