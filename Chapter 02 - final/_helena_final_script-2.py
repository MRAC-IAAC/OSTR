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

img_path = ('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/Chapter 02 - final/sample_tests/400x400pix_test3.png')

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
        cv.drawContours(drawing, simp_contours, i, color, 1, cv.LINE_8, hierarchy, 0)

    cv.imshow('Image', img)
    cv.imshow('Contours', drawing)
    cv.waitKey()

    list_contours = []
    list_contours.append(simp_contours)
    print(type(simp_contours[0]))
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
    pixel_ratio = 5 # in mm

    list_pts_x_new = []
    list_pts_y_new = []

    for i in list_pts_x[0]:
        list_pts_x_new.append(i[0])
    print('Starting list for X is: ', list_pts_x_new)

    for i in list_pts_y[0]:
        list_pts_y_new.append(i[0])
    print('Starting list for Y is: ', list_pts_y_new)

    # For points in X
    list_pts_x_new_next = list_pts_x_new.copy()
    list_pts_x_new_next.pop(0)
    list_pts_x_new_next.append(0)

    print('New points in X: ', list_pts_x_new_next)

    # For points in Y
    list_pts_y_new_next = list_pts_y_new.copy()
    list_pts_y_new_next.pop(0)
    list_pts_y_new_next.append(0)
    
    print('New points in Y: ', list_pts_y_new_next)
    
    # Calculate distances

    distance_X = []
    zip_object = zip(list_pts_x_new, list_pts_x_new_next)
    for list_pts_x_new_i, list_pts_x_new_next_i in zip_object:
        distance_X.append(abs(list_pts_x_new_i-list_pts_x_new_next_i))
    print('Distance in X: ', distance_X)

    distance_Y = []
    zip_object = zip(list_pts_y_new, list_pts_y_new_next)
    for list_pts_y_new_i, list_pts_y_new_next_i in zip_object:
        distance_Y.append(abs(list_pts_y_new_i-list_pts_y_new_next_i))
    print('Distance in X: ', distance_Y)

    distance_X_P2 = []
    distance_Y_P2 = []
    zip_object = zip(distance_X, distance_Y)
    for distance_X_i, distance_Y_i in zip_object:
        distance_X_P2.append(distance_X_i**2)
        distance_Y_P2.append(distance_Y_i**2)
    print('Distances squared are: ', distance_X_P2, distance_Y_P2)

    distance_root = []
    zip_object = zip(distance_X_P2, distance_Y_P2)
    for distance_X_P2_i, distance_Y_P2_i in zip_object:
        distance_root.append((distance_X_P2_i)+(distance_Y_P2_i))
    print('Distance squared added are: ', distance_root)

    distance_d = []
    for d in distance_root:
        distance_d.append(math.sqrt(d))
    print('Distances to move F in image are : ', distance_d)

    distances = []
    for d_r in distance_d:
        distances.append((d_r/pixel_ratio))
    print('Real distances to move F are : ', distances)

    # Calculate angles
    distance_a = []
    zip_object = zip(distance_X, distance_Y)
    for distance_X_a_i, distance_Y_a_i in zip_object:
        distance_a.append(abs(distance_X_a_i / distance_Y_a_i))
    # print('Distances for tangeant are: ', distance_a)

    angles_tan = []
    for tan_a in distance_a:
        angles_tan.append(abs(math.tan(tan_a)))
    print('Angles for rotations in R are: ', angles_tan)

    # Round values for distances
    distances_round = [round(num) for num in distances]
    print('Rounded distances are: ', distances_round)

    # Round values for angle
    angles_round_tan = [round(num) for num in angles_tan]
    print('Rounded angles are: ', angles_round_tan)
    
    return distances_round, angles_round_tan

def get_instructions(distances_round, angle_round_tan): 

    # Decide on common language with robot (check with Jeo)
    # F = Forward (takes distance in mm)
    # R = Turn right (takes angle in degrees)
    # U = PenUp
    # D = PenDown

    # Get list of strings for Distances
    str_of_distances1 = map(str, distances_round)  
    str_of_distances2 = ["F" + dist for dist in str_of_distances1]
    # print('String list of Distances is: ', str_of_distances2)
    
    string_distances_round = [str('F' +int) for int in str_of_distances2]
    str_of_distances = "\n".join(str_of_distances2)
    # print('Distance instructions are: ', str_of_distances)

    # Get list of strings for Angles
    str_of_angles1 = map(str, angle_round_tan)  
    str_of_angles2 = ["R" + a for a in str_of_angles1]
    # print('String list of Angles is: ', str_of_angles2)

    string_angle_round_tan = [str('R' +int) for int in str_of_angles2]
    str_of_angles = "\n".join(str_of_angles2)
    # print('Angle instructions are: ', str_of_angles)

    combined = []
    for i in range(len(str_of_angles2)):
        combined.append(str_of_angles2[i])
        combined.append(str_of_distances2[i])
    print(combined)

    instructions = []    
    first_intructions = [str(int) for int in combined]
    instructions = "\n".join(combined)
    print('Final instructions are: ', instructions)

    return instructions

def send_to_robot():

    # ?
    # Listen to the robot until it's done

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
list_contours, list_pts_x_new, list_pts_y_new = contours(img_binary,0)

# Calculations
distances_round, angle_round_tan = calculate(list_pts_x_new, list_pts_y_new)

# Get Instructions
get_instructions(distances_round, angle_round_tan)

print('\n', 'Ma chérie tout va bien', '\n')