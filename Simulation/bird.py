import cv2
import numpy as np

image = cv2.imread('test_images\crads.jpg')
# Perspective points to be warped
pts1 = np.float32([[468, 450],
                    [637, 485],
                    [374, 614],
                    [556, 656]])

width, height = 250,350
pts2 = np.float32([[0, 0],
                    [width, 0],
                    [0, height],
                    [width, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
output = cv2.warpPerspective(image, matrix, (width, height))

cv2.circle(image, (pts1[0][0], pts1[0][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[1][0], pts1[1][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[2][0], pts1[2][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[3][0], pts1[3][1]), 5, (0,0,255), cv2.FILLED)
cv2.imshow("frame" , image)
cv2.imshow("output" , output)
res = cv2.waitKey(0) 


image = cv2.imread('test_images\straight_lines1.jpg')
# Perspective points to be warped
pts1 = np.float32([[539, 481],
                    [718, 462],
                    [240, 670],
                    [1060, 676]])

width, height = 350,450
pts2 = np.float32([[0, 0],
                    [width, 0],
                    [0, height],
                    [width, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
output = cv2.warpPerspective(image, matrix, (width, height))

cv2.circle(image, (pts1[0][0], pts1[0][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[1][0], pts1[1][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[2][0], pts1[2][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[3][0], pts1[3][1]), 5, (0,0,255), cv2.FILLED)
cv2.imshow("frame" , image)
cv2.imshow("output" , output)
res = cv2.waitKey(0) 


image = cv2.imread('test_images\\test1.jpg')
# Perspective points to be warped
pts1 = np.float32([[539, 481],
                    [718, 462],
                    [240, 670],
                    [1060, 676]])

width, height = 350,450
pts2 = np.float32([[0, 0],
                    [width, 0],
                    [0, height],
                    [width, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
output = cv2.warpPerspective(image, matrix, (width, height))

cv2.circle(image, (pts1[0][0], pts1[0][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[1][0], pts1[1][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[2][0], pts1[2][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[3][0], pts1[3][1]), 5, (0,0,255), cv2.FILLED)
cv2.imshow("frame" , image)
cv2.imshow("output" , output)
res = cv2.waitKey(0) 


image = cv2.imread('test_images\sharpturn.jpg')
# Perspective points to be warped
pts1 = np.float32([[100, 340],
                    [440, 320],
                    [4, 450],
                    [620, 450]])

width, height = 350,450
pts2 = np.float32([[0, 0],
                    [width, 0],
                    [0, height],
                    [width, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
output = cv2.warpPerspective(image, matrix, (width, height))

cv2.circle(image, (pts1[0][0], pts1[0][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[1][0], pts1[1][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[2][0], pts1[2][1]), 5, (0,0,255), cv2.FILLED)
cv2.circle(image, (pts1[3][0], pts1[3][1]), 5, (0,0,255), cv2.FILLED)
cv2.imshow("frame" , image)
cv2.imshow("output" , output)
res = cv2.waitKey(0) 