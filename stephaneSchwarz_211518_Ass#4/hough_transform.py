#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from skimage.color import rgb2gray
from skimage.transform import rotate
from skimage import filter
from skimage.transform import (hough_line, hough_line_peaks)
from scipy.stats import mode
import pytesseract
import sys
import time

def binarizeImage(RGBimage):

	image = rgb2gray(RGBimage)
	threshold = filter.threshold_otsu(image)
	binarizedImage = image < threshold
	
	return binarizedImage

def getImage(imagePath):

	return misc.imread(imagePath)

def show_image(image):

	plt.imshow(image, cmap="gray")
	plt.show()

	return

def save_image(image):

	misc.imsave("Hough.png", image)
	return

def rotateImage(image, angle):

	return rotate(image, angle)

def imageToText(image):

	text = pytesseract.image_to_string(getImage(image))
	print(text)

if __name__ == '__main__':

	_, imageName = sys.argv
	
	image = getImage(imageName)

	show_image(image)

	binarizedImage = binarizeImage(image)

	t0 = int(round(time.time() * 1000))

	input_image = filter.sobel(binarizedImage)
	h, theta, d = hough_line(input_image)
	accum, angles, dists = hough_line_peaks(h, theta, d)
	angle = np.rad2deg(angles)
	
	moda = max(angle)
	
	if moda < 0:

		moda = moda + 90
	else:

		moda = moda - 90

	imageResulted = rotateImage(binarizedImage, moda)

	t1 = int(round(time.time() * 1000))

	imageVisualization = 255 - imageResulted

	save_image(imageVisualization)

	show_image(imageVisualization)

	imageToText("Hough.png")
