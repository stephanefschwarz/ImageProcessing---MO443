from scipy import misc
from scipy import ndimage
from skimage import exposure

import numpy as np
import matplotlib.pyplot as plt



# This function is responsable to get the path or name of an image.
# @return the path to find the image
# @parm nothing

def getInputData():
	
	return raw_input("Image path or image name: ")

# This function read an image from a file
# @return image vector
# @parm path or image file name

def readImageFromFile(imageFile):
	if imageFile == "exit":
		exit()

	try:
		return misc.imread(imageFile)

	except IOError:
		print "Image not found, try again!"
		return readImageFromFile(getInputData())

# Image histogram is a graphical representation of the number of pixels in an image.
# @param arg1 is the array of an image
# @param arg2 is the bins of the image
# @param arg3 

def showImageHist(image):
	
	plt.hist(image.ravel(), 256, [0, 255])
	plt.xlabel("Niveis de Cinza")
	plt.ylabel("Frequencia")
	plt.title("Histograma")
	plt.show()
	return

# Show the negative of a picture 
# @return nothing
# @parm image vector

def showNegativeImage(image):
	
	g = 255 - image	
	plt.imshow(g, cmap="gray")
	plt.show()
	return g

# Show statistics measurements of the image selected
# @return nothing
# @parm image vector

def showImageMeasurements(image):
	
	print "Max: " + str(image.max())
	print "Mean: " + str(round(image.mean(), 2))
	print "Min: " + str(image.min())
	hei, wid = image.shape
	print "Altura: " + str(hei)
	print "Largura: " + str(wid)
	return

# Change the intensity of an image
# @return nothing
# @parm image vector

def changeImageIntensity(image):
	
	maxValue = image.max()
	minValue = image.min()

	w, h = image.shape

	for x in range(w):
				
		for y in range(h):

			image[x][y] = round( (image[x][y] - 0) * (180 - 120) / (255 - 0) + 120) 

	plt.imshow(image, cmap="gray", vmin=120, vmax=180)
	plt.show()

	return image

# Get user response
# @retun nothing

def getUserResponse(nega, inten):

	response = raw_input("Would you like save the images? [s/n] ")

	if response == "s":

		misc.imsave("negative.png", nega)
		misc.imsave("intensity.png", inten)
	return

while 1 :

	globalImage = readImageFromFile(getInputData())	
 
	showImageHist(globalImage)

	nega = showNegativeImage(globalImage)
	
	showImageMeasurements(globalImage)

	inten = changeImageIntensity(globalImage)
	
	getUserResponse(nega, inten)
	
	



