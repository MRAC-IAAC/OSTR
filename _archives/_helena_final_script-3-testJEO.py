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

    print('Contours are in the form of a: ', type(contours))
    print('\n')

    # Simplify contours
    simp_contours = []
    for c in contours:
        epsilon = 0.01*cv.arcLength(c,True)
        approx_cnt = cv.approxPolyDP(c,epsilon,True)
        simp_contours.append(approx_cnt)
    print('Simplified contours are: ', simp_contours)
    print(type(simp_contours))
    print('\n')

    for i in range(len(simp_contours)):
        color = (rng.randint(255,255), rng.randint(255,255), rng.randint(255,255))
        cv.drawContours(drawing, simp_contours, i, color, 1, cv.LINE_8, hierarchy, 0)

    cv.imshow('Image', img)
    cv.imshow('Contours', drawing)
    cv.waitKey()
    
    list_contours = []
    for l in simp_contours:
        sublists = l.tolist()
        list_contours.append(sublists)
    print('List of contours is: ', list_contours)
    print('Type of contours is: ', type(list_contours))
    print('Length of contours is: ', len(list_contours))
    print('\n')

    # List of points in X
    points_in_X = []
    for i in list_contours:
        for a in i:
            points_in_X.append(a[0][0])
    print('Points in X are: ', points_in_X)
    print('\n')

    # List of points in Y
    points_in_Y = []
    for i in list_contours:
        for a in i:
            points_in_Y.append(a[0][1])
    
    print('Points in Y are: ', points_in_Y)
    print('\n')

    return list_contours, points_in_X, points_in_Y

def calculate(list_pts_x, list_pts_y):

    current_pt = [0,0]
    pixel_ratio = 5 # in mm

    list_pts_x_new = []
    list_pts_y_new = []

    for i in list_pts_x:
        list_pts_x_new.append(i)
    print('Starting list for X is: ', list_pts_x_new)
    print('\n')

    for i in list_pts_y:
        list_pts_y_new.append(i)
    print('Starting list for Y is: ', list_pts_y_new)
    print('\n')

    # For points in X
    list_pts_x_new_next = list_pts_x_new.copy()
    list_pts_x_new_next.pop(0)
    valX = list_pts_x_new_next[-1]
    valX100 = valX + 100
    list_pts_x_new_next.append(valX100)
    
    print('New points in X: ', list_pts_x_new_next)
    print('\n')

    # For points in Y
    list_pts_y_new_next = list_pts_y_new.copy()
    list_pts_y_new_next.pop(0)
    valY = list_pts_y_new_next[-1]
    valY100 = valY + 100
    list_pts_y_new_next.append(valY100)
    
    print('New points in Y: ', list_pts_y_new_next)
    print('\n')

    # Calculate distances
        # Distances in X
    distance_X = []
    zip_object = zip(list_pts_x_new, list_pts_x_new_next)
    for list_pts_x_new_i, list_pts_x_new_next_i in zip_object:
        print('i am here: ', list_pts_x_new_i, list_pts_x_new_next_i)
        distance_X.append(abs((list_pts_x_new_i) - (list_pts_x_new_next_i)))
    print('Distance in X: ', distance_X)
    print('\n')

       # Distances in Y
    distance_Y = []
    zip_object = zip(list_pts_y_new, list_pts_y_new_next)
    for list_pts_y_new_i, list_pts_y_new_next_i in zip_object:
            distance_Y.append(abs(list_pts_y_new_i-list_pts_y_new_next_i))
    print('Distance in X: ', distance_Y)
    print('\n')

       # Distances squared
    distance_X_P2 = []
    distance_Y_P2 = []
    zip_object = zip(distance_X, distance_Y)
    for distance_X_i, distance_Y_i in zip_object:
        distance_X_P2.append(distance_X_i**2)
        distance_Y_P2.append(distance_Y_i**2)
    print('Distances squared are: ', distance_X_P2, distance_Y_P2)
    print('\n') 

       # Distances square rooted
    distance_root = []
    zip_object = zip(distance_X_P2, distance_Y_P2)
    for distance_X_P2_i, distance_Y_P2_i in zip_object:
        distance_root.append((distance_X_P2_i)+(distance_Y_P2_i))
    print('Distance squared added are: ', distance_root)
    print('\n')

       # Distances to move Forward
    distance_d = []
    for d in distance_root:
        distance_d.append(math.sqrt(d))
    print('Distances to move F in image are : ', distance_d)
    print('\n')

       # Scaled distances to move Forward
    distances = []
    for d_r in distance_d:
        distances.append((d_r/pixel_ratio))
    print('Real distances to move F are : ', distances)
    print('\n')

    # Calculate angles
    distance_a = []
    zip_object = zip(distance_X, distance_Y)
    for distance_X_a_i, distance_Y_a_i in zip_object:
        distance_a.append(abs(distance_X_a_i / distance_Y_a_i))

       # Angles to Rotate
    angles_tan = []
    for tan_a in distance_a:
        angles_tan.append(abs(math.tan(tan_a)))
    print('Angles for rotations in R are: ', angles_tan)
    print('\n')

        # Rounded values for distances
    distances_round = [round(num) for num in distances]
    print('Rounded distances are: ', distances_round)
    print('\n')

        # Rounded values for angle
    angles_round_tan = [round(num) for num in angles_tan]
    print('Rounded angles are: ', angles_round_tan)
    print('\n')

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

    combined = ['D']
    for i in range(len(str_of_angles2)):
        combined.append(str_of_angles2[i])
        combined.append(str_of_distances2[i])
    print('Combined: ', combined)
    print('\n')

    instructions = []    
    first_intructions = [str(int) for int in combined]
    instructions = "\n".join(combined)
    print('Final instructions are: ', instructions)
    print('\n')

    # Save to CSV file
    file_name = 'Instructions_test1'

    with open(file_name+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerows(instructions)

    with open(file_name+'.csv', 'r') as f:
        reader = csv.reader(f)
        instructions = list(reader)

    return instructions

def send_to_robot():

    # ?
    # Listen to the robot until it's done

    done = ser.read()
    if done == "DONE":
        return True
    else:
        return False

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