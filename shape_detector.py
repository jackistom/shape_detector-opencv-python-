import cv2 as cv
import time
import imutils
import numpy as np
import os
import binascii
#import RPI.GPIO as GPIO
#import serial
def color_exctrion(frame):
    lower_blue = np.array([110, 43, 46])
    upper_blue = np.array([124, 255, 255])
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    COLOR_ARRAY = [[lower_red, upper_red, "red"], [lower_blue, upper_blue, "blue"],
                   [lower_green, upper_green, "green"]]
    frame_second=cv.GaussianBlur(frame,(5,5),0)
    frame_final=cv.morphologyEx(frame_second,cv.MORPH_OPEN,(5,5))
    gray=cv.cvtColor(frame_final,cv.COLOR_BGR2GRAY)
    hsv=cv.cvtColor(frame_final,cv.COLOR_BGR2HSV)
    ret,binary=cv.threshold(gray,0,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
    contours,hir=cv.findContours(binary,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    # contours=contours[0] if imutils.is_cv2() else contours[1]
    number=len(contours)
    if number > 0:
        for cnt in range(number):
            epsilon = 0.01 * cv.arcLength(contours[cnt], True)
            approx = cv.approxPolyDP(contours[cnt], epsilon, True)
            corners = len(approx)
            print(approx,"\n")
            shape_type=""
            print(approx)
            if corners>=2:
                if corners<=3:
                    shape_type = "triangle"
                if corners == 4:
                    shape_type = "rectangle"
                if corners >= 10:
                    shape_type = "circles"
                    # if 4 < corners < 10:
                if 4 < corners < 10:
                    shape_type = "other"
                mm = cv.moments(contours[cnt])
                cx = (mm['m10'] / mm['m00']+2)
                cy = (mm['m01'] / mm['m00']+2)
                for (color_min,color_max,name) in COLOR_ARRAY:
                    count=0
                    tamp=[]
                    mask=cv.inRange(hsv,color_min,color_max)
                    res_second=cv.bitwise_and(frame_final,frame_final,mask=mask)
                    res_blur=cv.GaussianBlur(res_second,(5,5),0)
                    ret_second,bright_second=cv.threshold(res_blur,10,255,cv.THRESH_BINARY)
                    gray_second=cv.cvtColor(bright_second,cv.COLOR_BGR2GRAY)
                    opened=cv.morphologyEx(gray_second,cv.MORPH_OPEN,(5,5))
                    closed=cv.morphologyEx(opened,cv.MORPH_CLOSE,(5,5))
                    contours_second,hir_second=cv.findContours(closed,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
                    # contours_second=contours[0] if imutils.is_cv2() else contours[1]
                    number_second=len(contours_second)
                    if number_second>=1:
                        total=0
                        for i in range(0,number_second):
                            total=total+len(contours_second[i])
                        if total>500:
                            print("Current color:",name)
                            cv.putText(frame, shape_type, (int(cx + 70), int(cy + 10)), cv.FONT_HERSHEY_PLAIN, 1.2,
                                       (255, 255, 255), 1)
                            cv.putText(frame, name, (int(cx + 5), int(cy + 10)), cv.FONT_HERSHEY_PLAIN, 1.2,
                                       (255, 255, 255), 1)
                            tamp=COLOR_ARRAY[count]
                            COLOR_ARRAY.pop(count)
                            COLOR_ARRAY.append(tamp)
                            count+=1
                            break
                        else:
                            continue
                    else:
                        continue
            else:
                break
        cv.imshow("img",frame)
        k=cv.waitKey(1000)&0xff
        if k== ord("q"):
            cv.destroyAllWindows()
            # break
            # else:
            #     print("corner<=2")
    else:
        print("final_no")

cap=cv.VideoCapture(1)
i=0
while (True):
    ret,frame=cap.read()
    cv.imshow("image",frame)
    k=cv.waitKey(1)&0xff
    if k==ord("q"):
        break
    elif k==ord("p"):
        i += 1
        cv.imwrite(str(i) + '.jpg', frame)
        image = cv.imread(str(i) + '.jpg', 1)
        color_exctrion(image)



