from scipy import misc

import re
import sys
import numpy as np
import matplotlib.pyplot as plt

# python Ass#2.1.py imagem_entrada.png plano_bits

LEN_INFO = 100

def formatCompat(image):

	if(image.ndim != 3):

		raise IndexError("Is not RGB")

def binToText(info):

	msg = ''.join(chr(int(bin, 2)) for bin in re.findall(r'.{8}', info))
	return msg

def getArgs(imageName):

	image = misc.imread(imageName)

	formatCompat(image)

	return image

def recupera(image, bitPosition):

	info = ''
	done = False
	flag = 0
	msg_len = 0

	for h in range(0, image.shape[0]):
		if (done):					
			break

		for w in range(0, image.shape[1]):
			if (done):					
				break

			for dim in range(0, image.shape[2]):

				info += ''.join('1' if image[h][w][dim] & (1 << bitPosition) else '0')
		
				if len(info) >= (LEN_INFO * 3) and flag == 0:

					msg_len = int(info, 2)
					info = ''	
					flag += 1	
					print("flag == 0")		

				if flag != 0 and (flag - 1) >= msg_len:

					done = True
					break

				if flag != 0:

					flag += 1

	print(binToText(info))
	return

def showPlaneBit(image):

	ims = np.mod(np.floor(image/1), 2)
	plt.imshow(ims)
	misc.imsave("ims0.png", ims)
	plt.show()

	ims = np.mod(np.floor(image/2), 2)
	plt.imshow(ims)
	misc.imsave("ims1.png", ims)
	plt.show()

	ims = np.mod(np.floor(image/4), 2)
	plt.imshow(ims)
	misc.imsave("ims2.png", ims)

	plt.show()

	ims = np.mod(np.floor(image/128), 2)
	plt.imshow(ims)
	misc.imsave("ims3.png", ims)
	plt.show()
	return


if __name__ == "__main__":

	_, imageName, bit = sys.argv

	image = getArgs(imageName)

	recupera(image, int(bit))