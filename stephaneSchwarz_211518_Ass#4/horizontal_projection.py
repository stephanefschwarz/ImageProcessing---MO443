import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from skimage.color import rgb2gray
from skimage.exposure import rescale_intensity
from skimage.transform import rotate
from scipy.stats import mode
from skimage import filter
import pytesseract
import sys

from PIL import Image

def getHorizontalProjection(image):

	lines = np.array(range(image.shape[0]))
	sumation = np.count_nonzero(image, axis=1)
	values = sumation
	
	return lines, values

def otsuBinarization(image):

	threshold = filter.threshold_otsu(image)
	binarizedImage = image < threshold

	return binarizedImage

def costfunction(image):

	sumation = np.count_nonzero(image, axis=1)
	std = np.std(sumation)

	return std

def getImage(path):

	return misc.imread(path)

def rgbToBinary(RGBimage):

	return otsuBinarization(rgb2gray(RGBimage))

def showBarGraph(x,y):

	plt.barh(x, y)
	name = "horizontal_projection.png"
	plt.savefig(name)
	plt.show()

def rotateImage(image, angle):

	return rotate(image, angle)

def imageToText(imagePath):

	image = getImage(imagePath)

	text = pytesseract.image_to_string(image)

	print(text)

	return

def show_image(image):

	plt.imshow(image, cmap="gray")
	plt.show()

	return

def getResult(image, angles):

	axis = angles.argmax() - 90
	print("Angulo")
	print(axis+90)

	resultedImage = rotateImage(binaryImage, axis)

	imageVisualization = 255 - resultedImage

	show_image(imageVisualization)

	misc.imsave("resultedImage.png", imageVisualization)
	
	imageToText("resultedImage.png")

	return resultedImage

if __name__ == '__main__':

	_, imageName = sys.argv

	image = getImage(imageName)

	binaryImage = rgbToBinary(image)

	data = np.empty((1, 180))
	
	for x in range(-90, 90):

		resultedImage = rotateImage(binaryImage, x)					

		sumation = costfunction(resultedImage)

		data[0, x+90] = sumation

	
	resultedImage = getResult(binaryImage, data)
	
	lines, sumation = getHorizontalProjection(resultedImage)

	showBarGraph(lines, sumation)
