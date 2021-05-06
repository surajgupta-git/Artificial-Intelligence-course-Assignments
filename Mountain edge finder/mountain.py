#!/usr/local/bin/python3
#
# Authors: [surgudla-tsadey-bgoginen]
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, April 2021

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy


# calculate "Edge strength map" of an image
def edge_strength(input_image):
    grayscale = numpy.array(input_image.convert('L'))
    filtered_y = numpy.zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return numpy.sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image.size[1] - 1))):
            image.putpixel((x, t), color)
    return image


# Reference: Course assignment CSCI-B 505 Applied Algorithms - Program taught by Prof. Jeremy Seik
class findRidge:
    def find_ridge(self, imageMatrix: [[int]]):
        rowLen = len(imageMatrix)
        colLen = len(imageMatrix[0])
        # 2D array to store values of each pixel
        store = [imageMatrix[0]]
        for i in range(1, rowLen):
            tmp = []
            for j in range(colLen):
                if j == 0:
                    tmp.append(imageMatrix[i][j] + max(store[i - 1][j], store[i - 1][j + 1]))
                elif j == colLen - 1:
                    tmp.append(imageMatrix[i][j] + max(store[i - 1][j], store[i - 1][j - 1]))
                else:
                    tmp.append(imageMatrix[i][j] + max(store[i - 1][j - 1], store[i - 1][j], store[i - 1][j + 1]))
            store.append(tmp)

        # backtrack to get the path
        path = [0] * rowLen
        path[rowLen - 1] = numpy.argmax(store[rowLen - 1])
        for i in range(rowLen - 2, -1, -1):
            j = path[i + 1]
            if j == 0:
                path[i] = numpy.argmax(store[i][j:j + 2]) + j
            elif j == colLen - 1:
                path[i] = numpy.argmax(store[i][j - 1:j + 1]) + j - 1
            else:
                path[i] = numpy.argmax(store[i][j - 1:j + 2]) + j - 1
        return path


# main program
gt_row = -1
gt_col = -1
if len(sys.argv) == 2:
    input_filename = sys.argv[1]
elif len(sys.argv) == 4:
    (input_filename, gt_row, gt_col) = sys.argv[1:]
else:
    raise Exception("Program requires either 1 or 3 parameters")

# load in image
input_image = Image.open(input_filename)
# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))
# output answer
input_image = draw_edge(input_image, argmax(edge_strength, axis=0).tolist(), (255, 0, 0), 5)

t2 = findRidge().find_ridge(edge_strength.T)
input_image = draw_edge(input_image, t2, (0, 0, 255), 7)

change_edge_strength = edge_strength
change_edge_strength[int(gt_row)][int(gt_col)] = change_edge_strength.sum()
t3 = findRidge().find_ridge(change_edge_strength.T)
imageio.imwrite("output.jpg", draw_edge(input_image, t3, (0, 255, 0), 2))
