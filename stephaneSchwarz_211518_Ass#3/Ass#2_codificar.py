from scipy import misc

import re
import sys
import numpy as np
import matplotlib.pyplot as plt

# python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png

LEN_INFO = 100

def getArgs(imageName, fileName):

	image = misc.imread(imageName)

	file = open(fileName, "r")	
	
	str_text = file.read()

	formatCompat(image)

	str_text = textToBin(str_text)

	infoLen = ''

	infoLen = ''.join(bin(len(str_text))[2:].zfill(LEN_INFO * 3))

	str_text = infoLen + str_text 

	return image, str_text

def formatCompat(image):

	if(image.ndim != 3):

		raise IndexError("Is not RGB")

# For each caracter in the text get the ASCI representation	
def textToBin(string):

	return ''.join(bin(ord(binary))[2:].zfill(8) for binary in string)

def binToText(info):

	msg = ''.join(chr(int(bin, 2)) for bin in re.findall(r'.{8}', info))
	return msg
	

def checkImageSize(image, text):

	'''
	Each pixel can store one bit of information,
	thus the maximo length of info need be slower
	than the quantity of pixel 
	'''
	if image.shape[0] * image.shape[1] * 3 < len(text):
		
		raise IndexError("Text size smaller than image length")

def convertImage(image, str_text, bitPosition):

	flag = 0
	done = False
	
	for h in range(0, image.shape[0]):
		if (done):					
			break

		for w in range(0, image.shape[1]):
			if (done):					
				break

			for dim in range(0, image.shape[2]):


				image[h][w][dim] = (image[h][w][dim] & ~(2 ** bitPosition)) | int(str_text[flag]) << bitPosition

				flag += 1

				if (flag >= len(str_text)):	

					done = True
					break

	plt.imshow(image)
	misc.imsave("ESTEGIMG.png", image)
	plt.show()



	return image

if __name__ == "__main__":

	_, imageName, fileName, bit = sys.argv

	image, str_text = getArgs(imageName, fileName)

	checkImageSize(image, str_text)

	convertImage(image, str_text, int(bit))