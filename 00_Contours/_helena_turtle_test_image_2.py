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
camera_image_width = 20 # Or get this from opencv camera input // piCamera is 1024 (x) x 768 (y)
distance_to_pixel_ratio = desired_width / camera_image_width

# Detect edges using Canny
canny_output = cv.Canny(img_gray, threshold, threshold * 2)

# Find contours
contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Draw contours
drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (rng.randint(255,255), rng.randint(255,255), rng.randint(255,255))
        #color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours, i, color, 3, cv.LINE_8, hierarchy, 0)
        print(contours)

# Set Turtle screen = image size
screen = turtle.Screen()
screen.setup(width = 500, height = 500)

# s = turtle.getscreen()
t = turtle.Turtle()

# Set the initial position of the Turtle
turtle.penup()
turtle.goto(-100,100)

for i in range(len(contours)):

    first_point = contours[i] # [X0, Y0]
    next_point = contours[i+1]  # [X1, Y1]

    current_position = [0,0]
    def get_distance(current_position, next_point):
            delta_y = next_point[1]-current_position[1]
            delta_x = next_point[0]-current_position[0]

            return math.sqrt((delta_x**2)+(delta_y**2))
        print(delta_x, delta_y)

    t.speed(1)
    t.forward(200)
    t.pen(pencolor="black", fillcolor="black", pensize=10, speed=1)

    t.clear()
    turtle.done()

# # Show in a window
# cv.imshow('Contours', drawing)
# print(type(drawing))

# Convert image to np array
myArray = np.asarray(drawing)

# Load source image
parser = argparse.ArgumentParser(description='Code for Finding contours in your image tutorial.')
parser.add_argument('--input', help='Path to input image.', default='YourImage.jpg')
args = parser.parse_args()

# src = cv.imread(cv.samples.findFile(args.input))
img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/00_Contours/sample_tests/100x100pix_test2.png')
if img is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# Convert image to gray and blur it
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_gray = cv.blur(img_gray, (3,3))

# Create Window
source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, img)
max_thresh = 255
thresh = 100 # initial threshold
cv.createTrackbar('Canny Thresh:', source_window, thresh, max_thresh, thresh_callback)
thresh_callback(thresh)


# Window same size
w, h = 2700, 3277
data = np.zeros((h, w, 3), dtype=np.uint8)
data[200:350, 200:350] = [255, 255, 255]
new_img = Image.fromarray(data, 'RGB')
# img.save('my.png')
# img.show()

cv.waitKey() 