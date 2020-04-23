
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
import math
import sys
import argparse


def interpolate(method, image, x, y):

    if(method == 0):

        return nearest_neighbor(image, x, y)

    if(method == 1):

        return bilinear(image, x, y)

    if(method == 2):

        return bicubic(image, x, y)

    if(method == 3):

        return lagrange(image, x, y)



def read_image(image_path):
    return misc.imread(image_path)





def plot_image(image, axis):
    
    plt.imshow(image, cmap="gray")
    plt.axis(axis)
    plt.show()




def rotate_image(method, image, angule):   
    
    height = image.shape[0]
    width = image.shape[1]
    
    rotated_image = np.zeros((height, width))
    indices = np.indices((height, width))    
    
    theta = np.deg2rad(angule)
    sin = math.sin(theta)
    cos = math.cos(theta)
    
    x_size = height // 2
    y_size = width // 2
        
    for x in range(height):        
        for y in range(width):
            
            x_line = round((x - x_size)  * cos + (y - y_size) * sin)
            y_line = round((x - x_size) * sin - (y - y_size) * cos)
            
            x_line += x_size
            y_line += y_size 
            
            rotated_image[x, y] = interpolate(method, image, x_line, y_line)
            
    return rotated_image





def nearest_neighbor(image, x_line, y_line):
    
    height = image.shape[0]
    width = image.shape[1]
    
    if(x_line >= 0 and x_line < height and y_line >= 0 and y_line < width):
        
        return image[x_line, y_line]
    else:        
        return 0    





def bilinear(image, x, y):
    
    dx, dy = calculate_dxdy(x, y)
    
    height = image.shape[0]
    width = image.shape[1]
    
    x_y = (x < height) and (x >= 0) and (y < width) and (y >= 0)
    xx_y = (x+1 < height) and (x+1 >= 0) and (y < width) and (y >= 0)
    x_yy = (x < height) and (x >= 0) and (y+1 < width) and (y+1 >= 0)
    xx_yy = (x+1 < height) and (x+1 >= 0) and (y+1 < width) and (y+1 >= 0)
    
    intensity = 0
    
    if(x_y and xx_y and x_yy and xx_yy):
        
        intensity = (1 - dx) * (1 - dy) * image[x, y]
        intensity += dx * (1 - dy) * image[x+1, y]
        intensity += dy * (1 - dx) * image[x, y+1]
        intensity += dx * dy * image[x+1, y+1]
        
    return intensity



def is_range(image, x, y):
    return x < image.shape[0] and x >= 0 and y < image.shape[1] and y >= 0


def bicubic(image, x, y):
    
    dx, dy = calculate_dxdy(x, y)
    
    intensity = 0
    for m in range(-1, 3):
        for n in range(-1, 3):
            x_m = x + m
            y_n = y + n
            
            if(is_range(image, x_m, y_n)):  

                intensity += image[x_m, y_n] * calculate_r(m-dx) * calculate_r(dy-n)                     

    return intensity


def calculate_r(s):
    
    p1 = calculate_p(s+2) ** 3
    p2 = calculate_p(s+1) ** 3
    p3 = calculate_p(s) ** 3
    p4 = calculate_p(s-1) ** 3
    return (1 / 6) * (p1 - 4 * p2 + 6 * p3 - 4 * p4)





def calculate_p(t):
    if (t > 0):
        return t
    return 0





def lagrange(image, x, y):
    
    dx, dy = calculate_dxdy(x, y)
    
    l1 = calculate_l(1, x, y, image)
    l2 = calculate_l(2, x, y, image)
    l3 = calculate_l(3, x, y, image)
    l4 = calculate_l(4, x, y, image)
    
    intensity = 0
    intensity = (-dy * (dy - 1) * l1) / 6
    intensity += ((dy + 1) * (dy - 1) * (dy - 2) * l2) / 2
    intensity += (-dy * (dy + 1) * (dy - 2) * l3) / 2
    intensity += (dy * (dy + 1) * (dy - 1) * l4) / 6
    
    return intensity
    
    



def calculate_l(n, x, y, image):
    
    dx, dy = calculate_dxdy(x, y)
    
    decision, f1, f2, f3, f4 = is_range_lagrange(image, x, y, n)
    
    if(decision):
    
        l = (-dx * (dx -1) * (dx - 2) * f1) / 6
        l += ((dx + 1) * (dx - 1) * (dx - 2) * f2) / 2
        l += (-dx * (dx + 1) * (dx - 2) * f3) / 2
        l += (dx * (dx + 1) * (dx -1) * f4) / 6

        return l
    return 0
  




def calculate_dxdy(x, y):
    
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    
    return dx, dy





def is_range_lagrange(image, x, y, n):
    
    height = image.shape[0]
    width = image.shape[1]
    
    f1 = (x-1 < height) and (x-1 >= 0) and (y+n-2 < width) and (y+n-2 >= 0)
    f2 = (x < height) and (x >= 0) and (y+n-2 < width) and (y+n-2 >= 0)
    f3 = (x+1 < height) and (x+1 >= 0) and (y+n-2 < width) and (y+n-2 >= 0)
    f4 = (x+2 < height) and (x+2 >= 0) and (y+n-2 < width) and (y+n-2 >= 0)
        
    if (f1 and f2 and f3 and f4):
        
        img_f1 = image[x-1, y+n-2]
        img_f2 = image[x, y+n-2]
        img_f3 = image[x+1, y+n-2]
        img_f4 = image[x+2, y+n-2]     
        
        return (True, img_f1, img_f2, img_f3, img_f4)
    
    return (False, 0, 0, 0, 0)





def rescaling_image(method, image, scaling_factor):
    
    new_x = round(scaling_factor * image.shape[0])
    new_y = round(scaling_factor * image.shape[1])
    
    new_image = np.zeros((new_x, new_y))  
    
    height = new_image.shape[0]
    width = new_image.shape[1]
    
    for x in range(0, height):
        for y in range(0, width):
            
            new_image[x, y] = interpolate(method, image, int(x / scaling_factor), int(y / scaling_factor))

    return new_image





def rescaling_image2(method, image, new_x, new_y):
    
    new_image = np.zeros((new_x, new_y))  
    
    scaling_factorx = float(new_x) / image.shape[0]
    scaling_factory = float(new_y) / image.shape[1]

    
    for x in range(0, new_x):
        for y in range(0, new_y):
            
            new_image[x, y] = interpolate(method, image, int(x / scaling_factorx), int(y / scaling_factory))

    return new_image



def get_user_answer():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help="image")
    parser.add_argument('-a', type=float, help="angle")
    parser.add_argument('-e', type=float, help="scaling factor")
    parser.add_argument('-d', type=int, help="width and height", nargs=2)
    parser.add_argument('-m', type=int, help="interpolation method", choices=range(0, 4))

    args = parser.parse_args()

    img = read_image(args.i)
    angle = args.a
    scale = args.e
    inter = args.m
    dimensions = args.d


    if(angle):

        return rotate_image(inter, img, angle)

    if(dimensions):

        return rescaling_image2(inter, img, dimensions[0], dimensions[1])

    if(scale):

        return rescaling_image(inter, img, scale)


if __name__ == '__main__':

    image = get_user_answer()
    
    plot_image(image, "image")
