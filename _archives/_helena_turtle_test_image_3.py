import csv
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import math
import matplotlib.pyplot as plt
import turtle
from PIL import Image
from numpy import savetxt

rng.seed(12345)

# current position at the start is the origin point and we have the convention
# that forward is aligned with X-axis
current_position = [0,0]
desired_width = 300 # in mm - user input
camera_image_width = 100 # Or get this from opencv camera input // piCamera is 1024 (x) x 768 (y) // current image is 100 x 100
distance_to_pixel_ratio = desired_width / camera_image_width

def find_dist(current_position, next_point):
    delta_x = abs(next_point[0]-current_position[0])
    delta_y = abs(next_point[1]-current_position[1])
    distance = math.sqrt((delta_x**2)+(delta_y**2))

    return distance

def find_angle(current_position, next_point):
    delta_x = abs(next_point[0]-current_position[0])
    delta_y = abs(next_point[1]-current_position[1])
    angle = math.tan(delta_y/delta_x)

    return angle

def img_contours(i):
    threshold = i

    img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/Chapter 02 - final/sample_tests/400x400pix_test1.png')
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray = cv.blur(img_gray, (3,3))
    img_binary = cv.threshold(img_gray, 128, 255, cv.THRESH_BINARY)[1]

   # Detect edges using Canny
    canny_output = cv.Canny(img_gray, threshold, threshold * 2)

    # Find contours
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

    # Simplify contours
    
    for c in contours:
        simp_contours = []
        epsilon = 0.01*cv.arcLength(c,True)
        appprox_cnt = cv.approxPolyDP(c,epsilon,True)
        simp_contours.append(appprox_cnt)
        print('simplified contours are: ', simp_contours)

    for i in range(len(simp_contours)):
        color = (rng.randint(255,255), rng.randint(255,255), rng.randint(255,255))
        #color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, simp_contours, i, color, 3, cv.LINE_8, hierarchy, 0)

    cv.imshow('Contours', drawing)

    list_contours = []
    list_contours.append(simp_contours)
    #print('list of contours', list_contours)

    list_contours = np.array([simp_contours])
    print(type(list_contours))
    #print(list_contours[0,0,0,0,0]) # get x value of first set of coordinates
    #print(list_contours[0,0,0,0,1]) # get y value of first set of coordinates
    
    # X value of all sets of coordinates
    list_pts_x = []
    list_pts_x.append(list_contours[0,0,:,:,0])
    print('the X coordinates are: ', '\n', list_pts_x)

    #print('\n')

    # Y value of all sets of coordinates
    list_pts_y = []
    list_pts_y.append(list_contours[0,0,:,:,1])
    print('the Y coordinates are: ', '\n', list_pts_y)

    # current_point = [0,0]
    # for ind, next_pt_X in enumerate(list_pts_x):
    #     print(next_pt_X)

    # print('\n')

    # for ind, next_pt_Y in enumerate(list_pts_y):
    #     print(next_pt_Y)

    def distance(current_pt, next_pt):
        dist_x = abs(next_pt_X[0] - current_point[0])
        dist_y = abs(next_pt_Y[1] - current_point[1])
        distance = math.sqrt((dist_x**2)+(dist_y**2))

        return distance

img_contours(0)

img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/Chapter 02 - final/sample_tests/400x400pix_test1.png')

# Load source image
parser = argparse.ArgumentParser(description='Code for Finding contours in your image tutorial.')
parser.add_argument('--input', help='Path to input image.', default='YourImage.jpg')
args = parser.parse_args()

# Convert image to gray and blur it
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_gray = cv.blur(img_gray, (3,3))

# Create Window
source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, img)
max_thresh = 255
thresh = 100 # initial threshold
# cv.createTrackbar('Canny Thresh:', source_window, thresh, max_thresh, img_contours)
# img_contours(thresh)

cv.waitKey()


