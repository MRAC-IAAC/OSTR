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

img_path = ('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/Chapter 02 - final/image-01.jpg')

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

    # print('Contours are in the form of a: ', type(contours))
    # print('\n')

    # Simplify contours
    simp_contours = []
    for c in contours:
        epsilon = 0.001*cv.arcLength(c,True)
        approx_cnt = cv.approxPolyDP(c,epsilon,True)
        simp_contours.append(approx_cnt)
    # print('Simplified contours are: ', simp_contours)
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
    # print('List of contours is: ', list_contours)
    # print('Type of contours is: ', type(list_contours))
    # print('Length of contours is: ', len(list_contours))
    # print('\n')

    # List of points in X
    points_in_X = []
    for i in list_contours:
        coordinates_X =[]
        for a in i:
            coordinates_X.append(a[0][0])
        points_in_X.append(coordinates_X)
    print('Points in X are: ', points_in_X)
    print('\n')

    # List of points in Y
    points_in_Y = []
    for i in list_contours:
        coordinates_Y =[]
        for a in i:
            coordinates_Y.append(a[0][1])
        points_in_Y.append(coordinates_Y)
    
    print('Points in Y are: ', points_in_Y)
    print('\n')

    return list_contours, points_in_X, points_in_Y

def calculate(points_in_X, points_in_Y):

    current_pt = [0,0]
    pixel_ratio = 2 # in mm

    X_next_coordinates = points_in_X.copy()
    Y_next_coordinates = points_in_Y.copy()

    # print('Starting list for X is: ', points_in_X)
    # print('\n')

    # print('Starting list for Y is: ', points_in_Y)
    # print('\n')

    # For points in X
    X_next_coordinates = []
    for i in points_in_X:
        i = i[1:]
        i.append(100)
        X_next_coordinates.append(i)

    # print('Next points are: ', X_next_coordinates)
    # print('\n')

    # For points in Y
    Y_next_coordinates = []
    for i in points_in_Y:
        i = i[1:]
        i.append(100)
        Y_next_coordinates.append(i)
    
    # print('New points in Y: ', Y_next_coordinates)
    # print('\n')

    # Calculate distances
        # Distances in X
    distance_X = []
    for a in range(len(points_in_X)):
        distances = []
        for b in range(len(points_in_X[a])):
            new_coordinates = abs(points_in_X[a][b] - X_next_coordinates[a][b])
            distances.append(new_coordinates)
        distance_X.append(distances)
    # print('Distance in X: ', distance_X)
    # print('\n')

    distance_X_Error = []
    for dis_x in distance_X:
        items = []
        for value in dis_x:
            if value == 0:
                value = 1
            items.append(value)
        distance_X_Error.append(items)
    # print('Distance X Error: ', distance_X_Error)

        # Distances in Y
    distance_Y = []
    for a in range(len(points_in_Y)):
        new_coordinates = []
        for b in range(len(points_in_Y[a])):
            new_coordinate = abs(points_in_Y[a][b] - Y_next_coordinates[a][b])
            new_coordinates.append(new_coordinate)
        distance_Y.append(new_coordinates)
    # print('Distance in Y: ', distance_Y)
    # print('\n')

    distance_Y_Error = []
    for dis_y in distance_Y:
        items = []
        for value in dis_y:
            if value == 0:
                value = 1
            items.append(value)
        distance_Y_Error.append(items)
    # print('Distance Y Error: ', distance_Y_Error)

       # Distances squared in X
    distance_X_P2 = []
    for a in range(len(distance_X)):
        sq = []
        for b in range(len(distance_X[a])):
            new_coordinates = abs(distance_X[a][b]**2)
            sq.append(new_coordinates)
        distance_X_P2.append(sq)
    # print('Distances X squared are: ', distance_X_P2)
    # print('\n')

       # Distances squared in Y
    distance_Y_P2 = []
    for a in range(len(distance_Y)):
        sq = []
        for b in range(len(distance_Y[a])):
            new_coordinates = abs(distance_Y[a][b]**2)
            sq.append(new_coordinates)
        distance_Y_P2.append(sq)
    # print('Distances Y squared are: ', distance_Y_P2)
    # print('\n')

       # Distances squared added
    distance_root = []
    for a in range(len(distance_X_P2)):
        sq_add = []
        for b in range(len(distance_X_P2[a])):
            new_coordinates = abs(distance_X_P2[a][b] + distance_Y_P2[a][b])
            sq_add.append(new_coordinates)
        distance_root.append(sq_add)
    # print('Distances squared added are: ', distance_root)
    # print('\n')

       # Distances to move Forward
    distance_d = []
    for d in distance_root:
        distances = []
        for i in d:
            distances.append(math.sqrt(i))
        distance_d.append(distances)
    # print('Distances to move F in image are : ', distance_d)
    # print('\n')

       # Scaled distances to move Forward
    distances = []
    for d_r in distance_d:
        move = []
        for i in d_r:
            move.append((i/pixel_ratio))
        distances.append(move)
    # print('Real distances to move F are : ', distances)
    # print('\n')

    # Calculate angles
    distance_a = []
    for a in range(len(distance_X)):
        angle_value = []
        for b in range(len(distance_X[a])):
            try:
                angle = abs(distance_Y[a][b] / distance_X[a][b])
            except ZeroDivisionError:
                angle = abs(distance_Y[a][b] / distance_X_Error[a][b])
            pass
            angle_value.append(angle)
        distance_a.append(angle_value)

       # Angles to Rotate
    angles_tan = []
    for a in range(len(distance_a)):
        tan_angle = []
        for b in range(len(distance_a[a])):
            value = abs(math.tan(distance_a[a][b]))
            tan_angle.append(value)
        angles_tan.append(tan_angle)
    # print('Angles for rotations in R are: ', angles_tan)
    # print('\n')

        # Rounded values for distances
    rounded_distances = []
    for i in distances:
        distances_round = [round(num) for num in i]
        rounded_distances.append(distances_round)
    # print('Rounded distances are: ', rounded_distances)
    # print('\n')
    
        # Rounded values for angle
    rounded_angles = []
    for a in angles_tan:
        angles_round_tan = [round(num) for num in a]
        rounded_angles.append(angles_round_tan)
    # print('Rounded angles are: ', rounded_angles)
    # print('\n')

    # Add in between distances to travel with Pen UP
    in_betweens_d = []
    last_values_dx = [dx[-1] for dx in points_in_X]
    last_values_dy = [dy[-1] for dy in points_in_Y]
    zipped_dxdy = zip(last_values_dx, last_values_dy)
    for x, y in zipped_dxdy:
        extra = [0]
        empty = []
        operation1 = (abs(x**2 - y**2))
        operation2 = math.sqrt(operation1)
        operation3 = operation2 / pixel_ratio
        operation4 = round(operation3)
        empty.append(operation4)
        in_betweens_d.append(empty)
    in_betweens_d.append(extra)
    print('In betweens D are: ', in_betweens_d)
    print('\n')

    full_list_D = []
    for d in range(len(rounded_distances)):
        full_list_D.append(rounded_distances[d])
        full_list_D.append(in_betweens_d[d])

    # Add FIRST distance to travel with Pen UP
    first_d = []
    first_value_dx = points_in_X[0][0]
    first_value_dy = points_in_Y[0][0]
    Foperation1 = (abs(first_value_dx**2 + first_value_dy**2))
    Foperation2 = math.sqrt(Foperation1)
    Foperation3 = Foperation2 / pixel_ratio
    Foperation4 = round(Foperation3)
    first_d.append(Foperation4)
    print('First Value to travel is: ', first_d)
    print('\n')

    full_list_D.insert(0, first_d)
    print('Full list of Distances is: ', full_list_D)
    print('\n')

    # Add in between angles to rotate with Pen UP
    in_betweens_a = []
    last_values_ax = [dx[-1] for dx in points_in_X]
    last_values_ay = [dy[-1] for dy in points_in_Y]
    zipped_dxdy = zip(last_values_dx, last_values_dy)
    for x, y in zipped_dxdy:
        extra = [0]
        empty = []
        operation1 = (x / y)
        operation2 = math.tan(operation1)
        operation3 = round(abs(operation2))
        empty.append(operation3)
        in_betweens_a.append(empty)
    in_betweens_a.append(extra)
    print('In betweens A are: ', in_betweens_a)
    print('\n')

    full_list_A = []
    for a in range(len(rounded_angles)):
        full_list_A.append(rounded_angles[a])
        full_list_A.append(in_betweens_a[a])
    print('Full List of Angles is: ', full_list_A)
    print('\n')

    # Add FIRST angle to rotate with Pen UP
    first_a = []
    first_value_ax = points_in_X[0][0]
    first_value_ay = points_in_Y[0][0]
    operation1_ = first_value_ay / first_value_ax
    operation2_ = math.tan(operation1_)
    operation3_ = round(operation2_)
    first_a.append(operation3_)
    print('First Value to rotate is: ', first_a)
    print('\n')

    full_list_A.insert(0, first_a)
    print('Full list of Angles is: ', full_list_A)
    print('\n')

    return full_list_D, full_list_A

def get_instructions(rounded_distances, rounded_angles): 

    # Decide on common language with robot (check with Jeo)
    # F = Forward (takes distance in mm)
    # R = Turn right (takes angle in degrees)
    # U = PenUp
    # D = PenDown

    # Get list of strings for Distances
    strings_d = []
    for i in rounded_distances:
        strgs = []
        string_ints = [str(num) for num in i]
        for i in string_ints:
            str_of_ints = 'F' + "".join(i)
            strgs.append(str_of_ints)
        strings_d.append(strgs)
    print('Distances strings are: ', strings_d)
    print('\n')

    # Get list of strings for Angles
    strings_a = []
    for i in rounded_angles:
        strgs = []
        string_ints = [str(num) for num in i]
        for i in string_ints:
            str_of_ints = 'R' + "".join(i)
            strgs.append(str_of_ints)
        strings_a.append(strgs)
    print('Angles strings are: ', strings_a)
    print('\n')

    combined = []
    for i in range(len(strings_a)):
        a = [list(x) for x in zip(strings_a[i], strings_d[i])]
        combined.append([inner for outer in a for inner in outer])
    print ('Combined List is: ', combined)
    print('\n')

    instructions = []
    for sublist in combined:
        for item in sublist:
            instructions.append(item)
    print ('Flat List is: ', instructions)

    return instructions

# Run code ____________________________________________________________

# Load Image
img = load_image(img_path)

# Process Image
img_binary = process_image(img)

# Contours
list_contours, points_in_X, points_in_Y = contours(img_binary,0)

# Calculations
distances_round, angle_round_tan = calculate(points_in_X, points_in_Y)

# Get Instructions
get_instructions(distances_round, angle_round_tan)

print('\n', 'Ma chérie tout va bien', '\n')