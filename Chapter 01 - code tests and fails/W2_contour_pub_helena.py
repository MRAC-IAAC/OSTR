#!/usr/bin/env python3

# Finding contours from an image and publishing to a rostopic

# Import the necessary libraries
import cv2  # OpenCV library
import numpy as np  # Numpy library
import argparse
from skimage.morphology import medial_axis

# Capture image
image = cv2.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/00_Contours/sample_tests/test01.png')
print(type(image))

# if image is loaded
if image is not None:

# Resize Image
    scale_percent = 65  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold on the image
    # https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
    ret, thresh = cv2.threshold(gray, 120, 255, 0)
    #cv2.imshow("Threshold", thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Apply erosion algorithm to remove small noises
    kernel = np.ones((9, 9), np.uint8)
    img_erosion = cv2.erode(thresh, kernel, iterations=1)
    # cv2.imshow("Erosion", img_erosion)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Apply blurring to soften the edges
    blurred = cv2.GaussianBlur(img_erosion, (11, 11), cv2.BORDER_DEFAULT)

    # Find Contours on the blurred image
    contours, hierarchy = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("Blurred", blurred)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Remove small contours
    final_contours = []
    for index, cnt in enumerate(contours):
        # if the contour has no other contours inside of it
        if hierarchy[0][index][2] == -1:
            # if the size of the contour is greater than a threshold
            if cv2.contourArea(cnt) > 2000:
                final_contours.append(cnt)

    # simplify the tree structure for contours array
    coordinates = []
    for cnt in final_contours:
        coordinates.append(np.squeeze(cnt, axis=(1,)))

    # simplify the contours (reduce resoloution)
    boundaries = []
    for cnt in coordinates:
        boundaries.append(cv2.approxPolyDP(cnt, 7, True))

    # draw the contours on the image
    for crv in boundaries:
        cv2.drawContours(resized, [crv], 0, (0, 0, 255), 3)
        cv2.imshow('Contours', resized)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # Center of contour
    # compute the center of the contour

    color_msg = ''
    for ind, c in enumerate(contours):
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        print(resized[cY, cX])
        print(resized.shape)

# # Get Colors
# # print (cx, cy)
# (b, g, r) = image[int(cY), int(cX)]
# print(b, g, r)
# colortext = str(b) + "," + str(g) + "," + str(r)
# # font
# font = cv2.FONT_HERSHEY_SIMPLEX
# # org
# org = (cX, cY)
# # fontScale
# fontScale = .4
# # Red color in BGR
# color = (0, 0, 255)
# # Line thickness of 2 px
# thickness = 2
# cv2.putText(resized, colortext, (cX, cY), font, fontScale,color, thickness, cv2.LINE_AA, False)

# color_msg += colortext + ';'

    # draw the contour and center of the shape on the image
    cv2.drawContours(resized, [crv], 0, (0, 0, 255), 3)
    cv2.circle(resized, (cX, cY), 7, (217, 23, 23), -1)

    # Display index of contours
    cv2.drawContours(resized, [crv], 0, (0, 0, 255), 3)
    cv2.putText(resized, "#{}".format(ind), (cX - 20, cY + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 252, 252), 2)

    cv2.imshow('Center', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Get middle line
    # line = medial_axis(resized).astype(np.uint8)
    # cv2.imshow('Middle', line)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #cv2.imwrite('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/SHEDIO/00_Contours/saved screens/test-05.png', resized)

else:
    print('Image not found')