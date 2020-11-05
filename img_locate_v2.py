import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import imutils

#read images
star_map = cv.imread('StarMap.png',0)
smallStart = cv.imread('Small_area.png',0)

#image that will be correlated
small = smallStart

global_max_val = 0
degree = 0
deltaAngle = 1

#find the orientation and location
while degree < 360:
    res = cv.matchTemplate(star_map, small,eval('cv.TM_CCORR_NORMED'))
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    degree = degree + deltaAngle
    small = imutils.rotate(smallStart, angle=degree)
    if max_val > global_max_val:
        global_max_val = max_val
        highestCorr = [min_val, max_val, min_loc, max_loc, degree]
    
#highest correlation window
top_left = highestCorr[3]
top_right = (top_left[0] + small.shape[1], top_left[1])
bottom_left = (top_left[0], top_left[1] + small.shape[0])
bottom_right = (top_left[0] + small.shape[1], top_left[1] + small.shape[0])
center =  (top_left[0] + small.shape[1]/2, top_left[1] + small.shape[0]/2)

#rotates a point around another point
def rotateAround(point, pivot, angle):
    cosTeta = np.cos(np.deg2rad(angle))
    sinTeta = np.sin(np.deg2rad(angle))
    rotatedPoint = (round((point[0] - pivot[0]) * cosTeta - (point[1] - pivot[1])*sinTeta + pivot[0]),
                    round((point[0] - pivot[0]) * sinTeta + (point[1] - pivot[1])*cosTeta + pivot[1]))
    return rotatedPoint
  
#rotate horizotal orientation  
rotated_top_left = rotateAround(top_left, center, -highestCorr[4])
rotated_top_right = rotateAround(top_right, center, -highestCorr[4])
rotated_bottom_left = rotateAround(bottom_left, center, -highestCorr[4])
rotated_bottom_right = rotateAround(bottom_right, center, -highestCorr[4])

#plot the window
cv.line(star_map,rotated_top_left, rotated_top_right, 255, 2)
cv.line(star_map,rotated_top_right, rotated_bottom_right, 255, 2)
cv.line(star_map,rotated_bottom_right, rotated_bottom_left, 255, 2)
cv.line(star_map,rotated_bottom_left, rotated_top_left, 255, 2)

plt.figure(1, figsize=(12,8))
plt.subplot(121)
plt.imshow(star_map,cmap = 'gray')
plt.title('Star Map with the location of the small image')
plt.subplot(122)
plt.imshow(smallStart,cmap = 'gray')
plt.title('Small image')

print('Corner coordinates:', rotated_top_left, rotated_top_right, rotated_bottom_left, rotated_bottom_right)