import cv2 as cv
import numpy as np
import argparse
import random as rng

rng.seed(12345)

# current position at the start is the origin point and we have the convention 
# that forward is aligned with X-axis
current_position = [0,0]
desired_width = 200 # in cm - user input
camera_image_width = 20 # Or get this from opencv camera input // piCamera is 1024 (x) x 768 (y)
distance_to_pixel_ratio = desired_width / camera_image_width

import math
from time import sleep

def find_angle(current_position, target_point, point_after_target):
    # First iteration no spline
    delta_y = target_point[1]-current_position[1]
    delta_x = target_point[0]-current_position[0]

    return math.tan(delta_y/delta_x)


def find_distance(current_position, target_point):
 
    delta_y = target_point[1]-current_position[1]
    delta_x = target_point[0]-current_position[0]

    return math.sqrt((delta_x**2)+(delta_y**2))

def send_to_robot(angle, distance, command_before = None, command_after = None):

    if command_before is not None:
        if command_before == "PEN DOWN":
            ser.print("PEN DOWN")

#     # Implement send and ACK from the robot
#     tries = 10
#     while ack != "OK" or tries<10:
#         ser.print(angle)
#         tries++
#         sleep(0.5)
#         ack = ser.read()

#     tries = 10
#     while ack != "OK" or tries<10:
#         ser.print(distance)
#         tries++
#         sleep(0.5)
#         ack = ser.read()

#     if command_after is not None:
#         if command_after == "PEN DOWN":
#             ser.print("PEN DOWN")

# def wait_for_instruction():
#     #Listen to the robot until it's done

#     done = ser.read()
#     if done == "DONE":
#         return True
#     else:
#         return False


def thresh_callback(val):
    threshold = val

    # Detect edges using Canny
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)

    # Find contours
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

    for contour in contours:
        # color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        # cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)

        # Each contour is a list of lists
        contour = [[1,2],[45,9]] #[[X, Y],[X, Y]]

        for i in range(len(contour)):

            target_point = contour[i] # [X0, Y0]
            point_after_target = contour[i+1]  # [X1, Y1]

            angle = find_angle(current_position, target_point, point_after_target)
            distance = find_distance(current_position, target_point)*distance_to_pixel_ratio
            command_before = decide_pen(boolean_list)
            command_after = decide_pen(boolean_list)
            
            send_to_robot(angle, distance, command_before, command_after)

            while not wait_for_instruction():
                print ("Waiting")

# Load source image
parser = argparse.ArgumentParser(description='Code for Finding contours in your image tutorial.')
parser.add_argument('--input', help='Path to input image.', default='Pixel Image')
args = parser.parse_args()

src = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/00_Contours/sample_tests/20x20pix_test2.png')
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# Convert image to gray and blur it
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3,3))

# Create Window
source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, src)
max_thresh = 255
thresh = 100 # initial threshold
cv.createTrackbar('Canny Thresh:', source_window, thresh, max_thresh, thresh_callback)
thresh_callback(thresh)

cv.waitKey()

import turtle

s = turtle.getscreen()
t = turtle.Turtle()

# Set the initial position of the Turtle
turtle.setpos((0,0))
turtle.penup()

# Go to the first target point and then all the next ones after that
def turtle_draw(starting_point, next_point, coor_X, coor_Y):

    starting_point = target_point # from contours
    next_point = point_after_target # from contours
    coor_X = target_point[1]-current_position[1] # delta_x
    coor_Y = target_point[0]-current_position[0] # delta_y
    
    return turtle.goto(coor_X, coor_Y)
    
turtle.pendown()
# turtle.goto(next 255 point [i +1] until end_of_line)


t.clear()
turtle.done()