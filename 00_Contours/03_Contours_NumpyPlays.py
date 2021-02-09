import csv
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import matplotlib.pyplot as plt
from PIL import Image
from numpy import savetxt

# Read image
img = cv.imread('/Users/helenahomsi/Desktop/IAAC/07 TERM 02/HARDWARE II/SHEDIO/SHEDIO/00_Contours/sample_tests/test01.png')
if img is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# Convert image to array with pixel values
