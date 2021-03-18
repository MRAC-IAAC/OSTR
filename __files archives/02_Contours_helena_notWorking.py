import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt

# Load image
image = cv2.imread(
    '/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/00_Contours/dancer.jpg')

# if image is loaded
if image is not None:
    # Resize Image
    scale_percent = 100  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # Convert the image to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 60, 180)

    # Apply binary threshold on the image
    # https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
    ret, thresh = cv2.threshold(gray, 200, 255, 0)

    fig, ax = plt.subplots(1, figsize=(12, 8))

    # Blur image
    blurred = cv2.GaussianBlur(thresh, (11, 11), cv2.BORDER_DEFAULT)

    # Get Contours
    contours, hierarchy = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Remove small contours
    final_contours = []
    for cnt in (contours):
        # if the contour has no other contours inside of it
        if hierarchy[0][1][2] == -1:
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

    def thresh_callback(val):
        threshold = val
        # Detect edges using Canny
        canny_output = cv2.Canny(gray, thresh, threshold * 2)

        # Find contours
        contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            color = (rng.randint(255,255), rng.randint(255,255), rng.randint(255,255))
            #color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            cv2.drawContours(drawing, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)

        cv2.imshow('Contours', drawing)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()

else:
    print('No image found')

# cv2.imshow('Thresh', edge)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
