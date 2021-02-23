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

# Define functions

def load_image(image):
    image_path = ('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/Chapter 02 - final/sample_tests/100x100pix_test2.png')
    img = cv.imread(image_path)
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
    canny_output = cv.Canny(img_gray, threshold, threshold * 2)
    # Find contours
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

    for i in range(len(contours)):
        color = (rng.randint(255,255), rng.randint(255,255), rng.randint(255,255))
        cv.drawContours(drawing, contours, i, color, 3, cv.LINE_8, hierarchy, 0)
    
    list_contours = []
    list_contours.append(contours)
    print(list_contours)

    # X value of all sets of coordinates
    list_X = []
    list_X.append(list_contours[0,0,:,:,0])
    print('the X coordinates are: ', '\n', list_X)

    print('\n')

    # Y value of all sets of coordinates
    list_Y = []
    list_Y.append(list_contours[0,0,:,:,1])
    print('the Y coordinates are: ', '\n', list_Y)

    return list_contours, list_X, list_Y

def calculate(list_X, list_Y):

    current_pt = [0,0]

    for x in range(len(list_X)-1):
        next_pt_X = x + 1
        print (next_pt_X)

    for y in range(len(list_Y)-1):
        next_pt_Y = y + 1
        print (next_pt_Y)

    # Calculate distance
    delta_x = abs(next_pt_X[0]-current_pt[0])
    delta_y = abs(next_pt_Y[1]-current_pt[1])
    distances = math.sqrt((delta_x**2)+(delta_y**2))

    # Calculate angle
    delta_x = abs(next_pt_X[0]-current_pt[0])
    delta_y = abs(next_pt_Y[1]-current_pt[1])
    angles = math.tan(delta_y/delta_x)

    return distances, angles

def get_instructions(distances, angles):


    return instructions

def send_to_robot(instructions):

    ### missing code

    if command_before is not None:
        if command_before == "PEN DOWN":
            ser.print("PEN DOWN")

    # Implement send and ACK from the robot
    tries = 10
    while ack != "OK" or tries<10:
        ser.print(angle)
        tries++
        sleep(0.5)
        ack = ser.read()

    tries = 10
    while ack != "OK" or tries<10:
        ser.print(distance)
        tries++
        sleep(0.5)
        ack = ser.read()

    if command_after is not None:
        if command_after == "PEN DOWN":
            ser.print("PEN DOWN")

    ### missing code

    return movements

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

# Run code


