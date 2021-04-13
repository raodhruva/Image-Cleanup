# coding: utf-8

import numpy as np
from PIL import Image
from collections import deque
import sys
import random

#sample input /Users/dhruva/Downloads/trial3.png ⁩
#sample output /Users/dhruva/Downloads/trial100.png 

# change LIGHT_TOL for different thresholds on what is considered "light"
LIGHT_TOL = 200

# GRAY_LOW decides how dark a gray we can accept
# GRAY_VARIANCE accounts for how far apart RGB can be from each other while making gray
GRAY_LOW = 120
GRAY_VARIANCE = 20

# function that classifies pixels as white, light or colored based on tolerance conditions
def createPixelNatureMatrix(image):
    x, y, d = image.shape
    pixelNatureMatrix = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            R, G, B, A = image[i, j]
            avg_shade = (int(R) + int(G) + int(B))/3
            if A == 0:
                continue
            if (R > LIGHT_TOL and G > LIGHT_TOL and B > LIGHT_TOL) or 
            (avg_shade > GRAY_LOW and abs(avg_shade - int(R)) < GRAY_VARIANCE and 
                         abs(avg_shade - int(G)) < GRAY_VARIANCE and abs(avg_shade - int(B)) < GRAY_VARIANCE):
                #Light is 1
                pixelNatureMatrix[i, j] = 1
            else:
                #colored is 2
                pixelNatureMatrix[i, j] = 2
    return pixelNatureMatrix

# function that returns neighbours of given pixel to add to stack
def getNeighbors(cur_x, cur_y):
    neighbors = []
    if cur_x != 0:
        neighbors.append([cur_x - 1, cur_y])
    if cur_x != image_length - 1:
        neighbors.append([cur_x + 1, cur_y])
    if cur_y != 0:
        neighbors.append([cur_x, cur_y - 1])
    if cur_y != image_height - 1:
        neighbors.append([cur_x, cur_y + 1])
    return neighbors

# iterator function that "increments" by sending pointer in a direction
def go_direction(direction, pixel):
    xa = 0
    ya = 0
    if direction == "left":
        xa = -1
    elif direction == "right":
        xa = 1
    elif direction == "up":
        ya = 1
    elif direction == "down":
        ya = -1
    else:
        return 0
    
    x, y = pixel
    
    while (0 < (x+xa) < image_length) and (0 < (y + ya) < image_height):
        if pixel_matrix[x + xa][y + ya] == 0:
            return 0
        if pixel_matrix[x + xa][y + ya] == 2:
            return 1
        x += xa
        y += ya
        
    return 0
    
'''performs an additional check on island pixels to make sure the pixel should actually be removed. 

    This is done by keeping track of each "island" of pixels. Then a set of random pixels are chosen from the island and
    traversed in one direction until a dark pixel, boundary, or white pixel is reached. If a dark pixel is found in all
    directions then the island shouldnt be removed.
'''
def island_boundary_check(image, island):
    l = len(island)
    test_points = random.sample(range(0, l), 10)
    counter = 0
    
    for point in test_points:
        pixel = island[point]
        if go_direction("left", pixel) + go_direction("right", pixel) + go_direction("up", pixel) + go_direction("down", pixel) == 4:
            counter += 1
    return counter

# performs an iterative DFS on the image to find and store the islands. They are stored in light_pixel_list

def Iterative_DFS(inputPath):
    image = np.array(Image.open(inputPath), dtype = np.uint8)

    global image_length
    global image_height
    global pixel_matrix
    image_length, image_height, depth = image.shape
    pixel_matrix = createPixelNatureMatrix(image)
    visited = np.zeros((image_length, image_height))
    light_pixel_list = []
    

    #deque allows for O(1) complexity on append and pop rather than a lists O(n)
    stack = deque()

    #append is a substitute for push
    stack.append([0, 0])
    visited[0, 0] = 1

    while stack:
        #node under consideration
        node = stack.pop()
        #get neighbors using x and y coordinate
        neighbors = getNeighbors(node[0], node[1])
        for pixel in neighbors:
            xtemp, ytemp = pixel
            if visited[xtemp, ytemp] == 1:
                continue
            visited[xtemp, ytemp] = 1
            pixelType = pixel_matrix[xtemp, ytemp]
            if pixelType == 1:
                #Light is 1
                #same DFS code but slightly different boundary condition
                island_stack = deque()
                island_stack.append(pixel)
                temp_light_pixel_list = [pixel]
                
                #if started in an island stay in an island
                while island_stack:
                    island_node = island_stack.pop()
                    island_neighbours = getNeighbors(island_node[0], island_node[1])
                    for island_pixel in island_neighbours:
                        xi_pixel, yi_pixel = island_pixel
                        if visited[xi_pixel, yi_pixel] == 1:
                            continue
                        visited[xi_pixel, yi_pixel] = 1
                        pixelType = pixel_matrix[xi_pixel, yi_pixel]
                        if pixelType == 1:
                            temp_light_pixel_list.append(island_pixel)
                            island_stack.append(island_pixel)
                            
                light_pixel_list.append(temp_light_pixel_list)
                        
            elif pixelType == 2:
                #Colored is 2
                continue
            stack.append(pixel)
    image = Image.fromarray(image)
    return light_pixel_list

# main function : pass input file path as argument 1 and output path as argument 2 while running this program.
if __name__ == '__main__':
    inputFile = sys.argv[1]
    outputPath = sys.argv[2]
    pixel_list = Iterative_DFS(inputFile)
    img = np.array(Image.open(inputFile), dtype = np.uint8)

    for island in pixel_list:
        #print(len(island))
        if len(island) > 500:
            if island_boundary_check(img, island) >= 5:
                continue    
        for pixel in island:
            x, y = pixel
            img[x, y] = [0, 0, 0, 0]
    finalimg = Image.fromarray(img)
    finalimg.save(outputPath)
