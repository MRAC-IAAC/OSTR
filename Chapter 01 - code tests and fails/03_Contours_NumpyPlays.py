import csv
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import matplotlib.pyplot as plt
import os
from PIL import Image
from numpy import savetxt

# %matplotlib inline

# Read image
img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/00_Contours/sample_tests/20x20pix_test2.png')

if img is None:
    print('Could not open or find the image:')
    exit(0)

# Get size of image
myArray = np.asarray(img)
# print(type(myArray))
print('\n')
print('The shape of the array is: ', myArray.shape)

# Resize Image
scale_percent = 100  # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resizedImg = cv.resize(img, dim, interpolation=cv.INTER_AREA)

print('Scaled array is now: ', resizedImg.shape)

# Convert image to np array
myArray = np.asarray(resizedImg)
# print(type(myArray))
# print(myArray.shape)
# print(myArray)
print('\n')

# Convert the image to grayscale
grayArray = cv.cvtColor(myArray, cv.COLOR_BGR2GRAY)

# Get color 255 or 0
imgGetColor = myArray.copy()
mat = imgGetColor[:, :]
# print(mat)
b, g, r = (imgGetColor[0, 0])
# r, g, b values are the same because image is black and white
print('The color of this pixel is: ', r)
print('\n')
print(type(myArray))

# for p in grayArray:
#     print (p)

# for p in grayArray:
#     print(p)
#     print(type(grayArray))

# Save to CSV file
file_name = 'ArrayShape1'
ArrayCSV = grayArray.tolist()
with open(file_name+'.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(grayArray)

with open(file_name+'.csv', 'r') as f:
    reader = csv.reader(f)
    ArrayCSV = list(reader)

cv.imshow('Image', myArray)
cv.waitKey(0)
# cv.destroyAllWindows()

for p in grayArray:
    for i in p:
        if i == 255:
            print('False')
        elif i == 0:
            print('True')
        elif 0 < i < 255:
            print('Discard')
        else:
            print(i)

# print ("List index-value are : ")
# for i in range(len(myArray)):
#     print (i, end = " ")
#     print (myArray[i])
