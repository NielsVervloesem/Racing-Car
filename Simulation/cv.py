
import cv2
import numpy as np
from numpy import array, argwhere

import numpy as np
from itertools import product
import time

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
  
# apply gaussian blur


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with 
    #depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
  
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), 
              minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((*img.shape, 3), dtype=np.uint8)
    
    draw_lines(line_img, lines)
    return line_img

def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    This function draws `lines` with `color` and `thickness`.    
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


cap = cv2.VideoCapture(r'C:\Users\11600624\Desktop\stage\004Code\Simulation\Racing-Car\Simulation\output_video.avi')

kernelSize = 3
low_threshold = 40
high_threshold = 100

rho = 1
theta = np.pi/180
threshold = 30
min_line_len = 25
max_line_gap = 60

lowerLeftPoint = [200, 425]
upperLeftPoint = [200, 170]
upperRightPoint = [250, 170]
lowerRightPoint = [250, 424]
pts = np.array([[lowerLeftPoint, upperLeftPoint, upperRightPoint, lowerRightPoint]], dtype=np.int32)

while(cap.isOpened()):
    ret, frame = cap.read()

    grayscaled = grayscale(frame)
    gaussianBlur = gaussian_blur(grayscaled, kernelSize)
    edgeDetectedImage = canny(gaussianBlur, low_threshold, high_threshold)
    #masked_image = region_of_interest(edgeDetectedImage, pts)
    masked_image = edgeDetectedImage[100:440,5:635]

    height, width = masked_image.shape
    end_y = int(height)
    start_point = (int(width/2), end_y)
    end_point = (int(width/2), end_y)
    front_point = (int(width/2), end_y)

    while (masked_image[end_y - 1, int(width/2)] == 0):
        end_point = (int(width/2), end_y)
        end_y -= 1

    cv2.line(masked_image, start_point, end_point, (255,255,255), 1)

    end_y += 25
    start_point = (int(width/2), end_y)
    distanceRight = 0
    distanceLeft = 0

    try:
        while (masked_image[end_y, int(width/2+distanceRight+1)] == 0):
            distanceRight += 1
            end_point = (int(width/2+distanceRight), end_y)
            cv2.line(masked_image, start_point, end_point, (255,255,255), 1)

    except:
        distanceRight = width/2
        end_point = (int(width/2+distanceRight), end_y)
    cv2.line(masked_image, start_point, end_point, (255,255,255), 1)

    try:
        while (masked_image[end_y, int(width/2 + distanceLeft-1)] == 0):
            distanceLeft -= 1
            end_point = (int(width/2+distanceLeft), end_y)
            cv2.line(masked_image, start_point, end_point, (255,255,255), 1)

    except:
        distanceLeft = width / 2
        end_point = (int(width/2+distanceLeft), end_y)


    if(distanceRight > width /2):
        distanceRight = width /2
    if(distanceLeft > width/2):
        distanceLeft = width/2
    cv2.line(masked_image, start_point, end_point, (255,255,255), 1)

    '''
    try:
        while(masked_image[end_y, 225] == 0):
            print(masked_image[front_point])
            end_y = end_y - 1
            front_point = (end_y, 225)
            print(front_point)
            cv2.line(masked_image, start_point, front_point, (255,0,0), 2)
    except:
        print(front_point)
        cv2.line(masked_image, start_point, front_point, (255,0,0), 2)
        print(":(")
        ex = True
    '''

    #houged = hough_lines(masked_image, rho, theta, threshold, min_line_len, max_line_gap)
    cv2.imshow("masked_image2", masked_image)

    '''
    cv2.imshow("grayscaled", grayscaled)
    cv2.imshow("gaussianBlur", gaussianBlur)
    cv2.imshow("edgeDetectedImage", edgeDetectedImage)
    cv2.imshow("masked_image", masked_image)
    cv2.imshow("houged", houged)
    '''


    res = cv2.waitKey(0) 
    
 
cap.release()
cv2.destroyAllWindows()



