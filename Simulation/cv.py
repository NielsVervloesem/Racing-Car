
import cv2
import numpy as np
from numpy import array, argwhere

import numpy as np
from itertools import product
print(cv2.__version__)
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

cap = cv2.VideoCapture(r'C:\Users\11600624\Desktop\stage\004Code\Simulation\Racing-Car\Simulation\output_video.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    canny_image = CannyEdge(frame)
    cropped_Image = region_of_interest(canny_image)

    test = np.transpose(np.nonzero(cropped_Image))

    left = (0,9999999)
    right = (0,-50000000)
    for i in test:
        if(i[1] > right[1]):
            right = i
        if(i[1] < left[1]):
            left = i     


    right = (right[1], right[0])
    left = (left[1],left[0])

    print(right)
    print(left)
    # Draw dots onto image
    #red
    cv2.circle(frame, right, 2, (0, 0, 255), -1)
    #green
    cv2.circle(frame, left, 2, (0, 255, 0), -1)
    cv2.line(frame, right, left, (255,0,0), 2)


    cv2.imshow("canny", canny_image)
    cv2.imshow('frame', frame)
    cv2.imshow('cropped', cropped_Image)

    print(slope(right[0], right[1], left[0], left[1]))

    res = cv2.waitKey(0) 

 
cap.release()
cv2.destroyAllWindows()



