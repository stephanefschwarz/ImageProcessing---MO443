from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage import filter
from skimage import measure

# get image
def getInputData():	
	
	return raw_input("Image path or image name: ")

# Read image from file
def readImageFromFile(imageFile):

	if imageFile == "exit":
		exit()

	try:
		return misc.imread(imageFile)
		
	except IOError:
		print "Image not found, try again!"
		return readImageFromFile(getInputData())

# Plot an image
def plotImage(image):
	
	plt.imshow(image, cmap="gray")
	plt.show()

# Rgb to gray 
def rgbToGray(image):
	
	grayImage = rgb2gray(image)

	misc.imsave("grayImage.png", grayImage)

	plt.imshow(grayImage, cmap="gray")
	plt.show()
	
	return grayImage

# Get contours
def getContours(binaryImage):

	contoursList = measure.find_contours(binaryImage, 0.9)

	figure, axis = plt.subplots()

	axis.imshow(binaryImage, cmap="gray")

	for x, contoursList in enumerate(contoursList):
		
		axis.plot(contoursList[:, 1], contoursList[:, 0], color="r", linewidth=2)

	plt.savefig("contours.png")

	plt.show()


	return

# Get properties
def getProperties(image):

	imageLabel = measure.label(image)

	properties = measure.regionprops(imageLabel)

	length = len(properties)

	print "Total de regioes: ", length

	for i in range(0, length):
		
		print "regiao: {:2d}".format(i), " perimetro: {:7.0f}".format(properties[i].perimeter), " area: {:7.0f}".format(properties[i].area)

	return properties

# Show number centroid
def numberCentorid(image, properties):
	
	figure, axis = plt.subplots()

	text = len(properties)

	for n in range(0,text):
		
		centro = properties[n].centroid
		
		x = centro[1]
		y = centro[0]

		axis.text(x-6, y+4, n, color="w", fontsize=10)

	axis.imshow(image, cmap="gray")

	plt.savefig("measure.png")

	plt.show()

def classifyObjects(properties):

	size = len(properties)

	axisX = []
	axisY = []

	smallArea = []
	largeArea = []
	mean = []



	for n in range(0, size):

		regionArea = properties[n].area 

		if(regionArea < 1500):
			
			smallArea.append(regionArea)

		elif (regionArea >= 3000):
			
			largeArea.append(regionArea)

		else:
			mean.append(regionArea)


	length = len(smallArea)
	print "numero de regioes pequenas ", str(length)

	length = len(mean)
	print "numero de regioes medias ", str(length)

	length = len(largeArea)
	print "numero de regioes grandes ", str(length)

	axisX = smallArea + mean + largeArea

	plt.hist(axisX, 3)
	plt.savefig("histgram.png")
	plt.show()

	return



globalImage = readImageFromFile(getInputData())	

binaryImage = rgbToGray(globalImage)

getContours(binaryImage)

properties = getProperties(binaryImage)

numberCentorid(binaryImage, properties)

classifyObjects(properties)
