import csv
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import matplotlib.pyplot as plt
from PIL import Image
from numpy import savetxt

rng.seed(12345)

def thresh_callback(val):
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

    # cv.imwrite('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/00_Contours/saved screens/test-03.png', drawing)

    # Show in a window
    cv.imshow('Contours', drawing)
    print(type(drawing))

    # Convert image to np array
    myArray = np.asarray(drawing)
    print(type(myArray))
    print(myArray.shape)
    print(myArray)

    # Save to CSV file
    file_name = 'CntArrayShape1'
    ArrayCSV = myArray.tolist()
    with open(file_name+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(ArrayCSV)

    with open(file_name+'.csv', 'r') as f:
        reader = csv.reader(f)
        ArrayCSV = list(reader)

    print(ArrayCSV)
    arrayShape = []
    for row in examples:
        nwrow = []
        for r in row:
            nwrow.append(eval(r))
        arrayShape.append(nwrow)
    print(arrayShape)

    # # img_path = '/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/00_Contours/saved screens/test-03.png'
    # # img = cv.imread(img_path, 0) # image is grayscale. change 0 to 1 for RGB
    # gcodeImage = drawing.shape / 255.0
    # np.set_printoptions(threshold=sys.maxsize)
    # print(type(gcodeImage))

# Load source image
parser = argparse.ArgumentParser(description='Code for Finding contours in your image tutorial.')
parser.add_argument('--input', help='Path to input image.', default='YourImage.jpg')
args = parser.parse_args()

# src = cv.imread(cv.samples.findFile(args.input))
img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/00_Contours/dancer.jpg')
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

# print(type(img))
# print(img.shape) # 3277, 2700 ,3

# mat = np.zeros(shape=(img.shape))
# print(mat)

# Window same size
w, h = 2700, 3277
data = np.zeros((h, w, 3), dtype=np.uint8)
data[200:350, 200:350] = [255, 255, 255]
new_img = Image.fromarray(data, 'RGB')
# img.save('my.png')
# img.show()



cv.waitKey()