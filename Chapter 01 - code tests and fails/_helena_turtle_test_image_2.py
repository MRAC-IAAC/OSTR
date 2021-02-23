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

def get_distance(current_position, next_point):
    delta_y = abs(next_point[1]-current_position[1])
    delta_x = abs(next_point[0]-current_position[0])

    return math.sqrt((delta_x**2)+(delta_y**2))

def thresh_callback(val,t):
    threshold = val
    
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

        for i in range(len(contours)-1):

            first_point = contours[i] # [X0, Y0]
            next_point = contours[i+1]  # [X1, Y1]
            
            print(i)

        for i in contours:
            print(i)

        #print(contours)

    # Show in a window
    cv.imshow('Contours', drawing)
    #print(type(drawing))

    # Convert image to np array
    myArray = np.asarray(drawing)
    # print(type(myArray))
    # print(myArray.shape)
    # print(myArray)

    # Save to CSV file
    file_name = 'CntArrayShape1'
    ArrayCSV = myArray.tolist()
    with open(file_name+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(ArrayCSV)

    with open(file_name+'.csv', 'r') as f:
        reader = csv.reader(f)
        ArrayCSV = list(reader)

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

# Load turtle screen
screen = turtle.getscreen()

# Set turtle
t = turtle.Turtle()
t.setposition(0,0)

# Call function
thresh_callback(100,t)

# Unchanged turtle commands
t.speed(1)
t.pen(pencolor="black", fillcolor="black", pensize=5, speed=1)

# Turtle commands (cheating) backwards L
t.penup()
t.goto(300,100)
t.pendown()
t.right(90)
t.forward(400)
t.right(90)
t.forward(400)

t.clear()
turtle.done()

# Turtle not cheating


# Create Window
source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, img)
max_thresh = 255
thresh = 100 # initial threshold


cv.waitKey()