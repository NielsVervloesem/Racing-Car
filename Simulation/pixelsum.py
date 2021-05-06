
import cv2 as cv
import numpy as np
from numpy import array, argwhere
import math
from math import cos, sin, pi
import numpy as np
from itertools import product


def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

def corners(np_array):
    ind = np.argwhere(np_array)
    res = []
    for f1, f2 in product([min,max], repeat=2):
        res.append(f1(ind[ind[:, 0] == f2(ind[:, 0])], key=lambda x:x[1]))
    return res

def CannyEdge(image):
  gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
  blur = cv2.GaussianBlur(gray, (5,5), 0)
  cannyImage = cv2.Canny(blur, 30, 60)
  return cannyImage

def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    roi = np.array([[(0, height-75),(width/2, height/2),(width-20, height-75),]], np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, roi, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def angle(startx, starty, length, angle):
    x = round(startx + length * cos(angle * pi / 180.0))
    y = round(starty + length * sin(angle * pi / 180.0))

    return (x,y)

#TODO pkl file prolly

#LEFT TO RIGHT, BUT FIX IN REALITY

'''
-90 = -180 = input[0]
-40 = -130 = input[1]
-15 = -105 = input[2]
  0 = -90 input[3]
 15 = -75 =input[4]
 40 = -50 input[5]
 90 = 0 = input[6]
'''
input = [130,93,130,130,109,77,50,60]

height = input[3]
if(input[0] > input[6]):
    width = input[0] * 2
else: 
    width = input[6]*2
width = 300
img = np.zeros((height,width,3), np.uint8)

x = width/2
y = height

p1 = angle(x, y, input[0], -180)
p2 = angle(x, y, input[1], -130)
p3 = angle(x, y, input[2], -105)
p4 = angle(x, y, input[3], -90)
p5 = angle(x, y, input[4], -75)
p6 = angle(x, y, input[5], -50)
p7 = angle(x, y, input[6], 0)

pts = np.array([p1,p2,p3,p4,p5,p6,p7], np.int32)
cv.polylines(img,[pts],True,(0,255,255))

cv.circle(img,(p1), 2, (0,0,255), -1)
cv.circle(img,(p2), 2, (0,0,255), -1)
cv.circle(img,(p3), 2, (0,0,255), -1)
cv.circle(img,(p4), 2, (0,0,255), -1)
cv.circle(img,(p5), 2, (0,0,255), -1)
cv.circle(img,(p6), 2, (0,0,255), -1)
cv.circle(img,(p7), 2, (0,0,255), -1)


cv.imshow("pixel summation test", img)
cv.waitKey(0)




