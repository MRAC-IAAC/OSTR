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

# Read image
img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/SHEDIO/00_Contours/sample_tests/test01.png')

if img is None:
    print('Could not open or find the image:')
    exit(0)

# Get size of image
myArray = np.asarray(img)
# print(type(myArray))
print('\n')
print('The shape of the array is: ', myArray.shape)

 # Resize Image
scale_percent = 20  # percent of original size
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

# Get color 255 or 0
imgGetColor = resizedImg.copy()
mat = imgGetColor[:,:]
# print(mat)
b,g,r = (imgGetColor[0, 0])
print(r) # r, g, b values are the same because image is black and white

# print(myArray)

# Convert the image to grayscale
grayArray = cv.cvtColor(myArray, cv.COLOR_BGR2GRAY)

for p in grayArray: 
    print(p)

# for x,y in resizedImg.shape[:,:]:
#     b, g, r = resizedImg[int(x), int(y)]
#     print ('The color of this pixel is: ', r) # r, g, b values are the same because image is black and white

# Save to CSV file
file_name = 'ArrayShape1'
ArrayCSV = myArray.tolist()
with open(file_name+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(ArrayCSV)

with open(file_name+'.csv', 'r') as f:
        reader = csv.reader(f)
        ArrayCSV = list(reader)

cv.imshow('Image', myArray)
cv.waitKey(0)
# cv.destroyAllWindows()

# print ("List index-value are : ") 
# for i in range(len(myArray)): 
#     print (i, end = " ") 
#     print (myArray[i]) 
