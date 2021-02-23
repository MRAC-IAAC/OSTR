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

# Define functions ___________________________________________________

img_path = ('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/Chapter 02 - final/sample_tests/400x400pix_test1.png')

def load_image(img_path):
    img = cv.imread(img_path)
    print('\n', 'Image is loaded!', '\n')
    if img is None:
        print('Image not found:', args.input)
        exit(0)
    return img

def process_image(img):

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.blur(img_gray, (3,3))
    img_binary = cv.threshold(img_blur, 128, 255, cv.THRESH_BINARY)[1]
    
    return img_binary

def contours(img_binary, i):
    threshold = i

    # Detect edges using Canny
    canny_output = cv.Canny(img_binary, threshold, threshold * 2)
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
        cv.drawContours(drawing, simp_contours, i, color, 3, cv.LINE_8, hierarchy, 0)

    cv.imshow('Contours', drawing)

    list_contours = []
    list_contours.append(simp_contours)
    # print('list of contours', list_contours)

    list_contours = np.array([simp_contours])
    print(type(list_contours))
    # print(list_contours[0,0,0,0,0]) # get x value of first set of coordinates
    # print(list_contours[0,0,0,0,1]) # get y value of first set of coordinates
    
    # X value of all sets of coordinates
    list_pts_x = []
    list_pts_x.append(list_contours[0,0,:,:,0])
    print('the X coordinates are: ', '\n', list_pts_x)

    print('\n')

    # Y value of all sets of coordinates
    list_pts_y = []
    list_pts_y.append(list_contours[0,0,:,:,1])
    print('the Y coordinates are: ', '\n', list_pts_y)

    return list_contours, list_pts_x, list_pts_y

def calculate(list_pts_x, list_pts_y):

    current_pt = [0,0]
    pixel_ratio = 50 # in mm

    for x in range(len(list_pts_x)-1):
        next_pt_X = list_pts_x[x + 1]
        # point_after_X = list_pts_x[x + 2]  # ? incorrect
        print (next_pt_X) #point_after_X)

    for y in range(len(list_pts_y)-1):
        next_pt_Y = list_pts_y[y + 1]
        # point_after_Y = list_pts_y[y + 2]  # ? incorrect
        print (next_pt_Y) #point_after_Y)

    # Calculate distance
    delta_x = abs(next_pt_X[0]-current_pt[0])
    delta_y = abs(next_pt_Y[1]-current_pt[1])

    # delta_next_x = abs(point_after_X[0]-current_pt[0])
    # delta_next_y = abs(point_after_Y[0]-current_pt[0])

    distance = (math.sqrt((delta_x**2)+(delta_y**2)))/pixel_ratio

    # Calculate angle
    delta_x = abs(next_pt_X[0]-current_pt[0])
    delta_y = abs(next_pt_Y[1]-current_pt[1])

    # For robot to keep moving forward, angle needs to be == 0
    # Simplify contours to have less points in 'straight line'

    # delta_next_x = abs(point_after_X[0]-current_pt[0])
    # delta_next_y = abs(point_after_Y[0]-current_pt[0])

    angle = math.tan(delta_y/delta_x)

        # if angle == 0:
        #     next_angle = math.tan(delta_next_y/delta_next_x)
        #     new_distance = (math.sqrt((delta_next_x**2)+(delta_next_y**2)))*pixel_ratio

    return distance, angle

def get_instructions(distance, angle): 

    # Decide on common language with robot (operated by Juan)
    # F = Forward (takes distance in mm)
    # R = Turn right (takes angle in degrees)
    # U = PenUp
    # D = PenDown

    # When angle != 0
    # Robot needs to turn right (R)

    for a, d in angle, distance:
        if a != 0:
            print ('R', a, '\n') # check 360 R / L (?)
        elif a > 0:
            print ('F', d, '\n')

    return instructions

def wait_for_instruction():
    #Listen to the robot until it's done

    done = ser.read()
    if done == "DONE":
        return True
    else:
        return False

def turtle_test(distance, angle):
    # Set Turtle screen = image size
    s = turtle.getscreen()

    # Set turtle
    t = turtle.Turtle()

    # Unchanged turtle commands
    t.speed(10)
    t.pen(pencolor="black", fillcolor="black", pensize=5, speed=1)

    # Turtle movements
    t.forward(distance)
    t.right(angle)

    t.clear()
    turtle.done()

    # If everything works, return ok!
    message = "Test ok"

    return message

# Run code ____________________________________________________________

# Load Image
img = load_image(img_path)

# Process Image
img_binary = process_image(img)

# Contours
list_contours, list_pts_x, list_pts_y = contours(img_binary,0)

# Run Calculations
calculate(list_pts_x, list_pts_y)