import numpy as np
import cv2 as cv
import Hands
import time
import matplotlib.pyplot as plt

def standardize(tile: np.ndarray, new_height=75, new_width=75, pad_value=0):
    """Either pads or trims an input image array to a specific height and width.
    """
    height = tile.shape[0]
    width = tile.shape[1]
    h_trim = 0
    w_trim = 0
    h_diff = int((new_height - height) / 2)
    w_diff = int((new_width - width) / 2)
    if h_diff < 0:
        h_trim = h_diff // -2
        h_diff = 0
    if w_diff < 0:
        w_trim = w_diff // -2
        w_diff = 0

    return np.pad(tile, ((h_diff, h_diff+((new_height-height)%2)), (w_diff, w_diff+((new_width-width)%2))), 'constant', constant_values=pad_value)[h_trim:new_height+1-h_trim, w_trim:new_width+1-w_trim]

def process_tile(image: np.ndarray):
    """Trims tile image and then pads to 75x75"""
    done = False
    tile_image = np.copy(255 - image)
    while not done:
        height = tile_image.shape[0]
        width = tile_image.shape[1]
        crop = [0, 0, 0, 0]
        min_left = np.sum(tile_image[:,0:1])
        min_top = np.sum(tile_image[0])
        min_right = np.sum(tile_image[:,width-1:width])
        min_bottom = np.sum(tile_image[height-1])
        for i in range(1, 5):
            left = np.sum(tile_image[:,i:i+1])
            top = np.sum(tile_image[i])
            right = np.sum(tile_image[:,width-1-i:width-i])
            bottom = np.sum(tile_image[height-1-i])
            if left <= min_left:
                min_left = left
                crop[0] = i
            if top <= min_top:
                min_top = top
                crop[1] = i
            if right <= min_right:
                min_right = right
                crop[2] = i
            if bottom <= min_bottom:
                min_bottom = bottom
                crop[3] = i
        tile_image = tile_image[crop[1]:height-crop[3],crop[0]:width-crop[2]]
        if (crop[0] == 0 and crop[1] == 0 and crop[2] == 0 and crop[3] == 0) or height < 10 or width < 10:
            done = True
    if tile_image.shape[0] < 10 or tile_image.shape[1] < 10:
        return standardize(255 - image)
    return standardize(tile_image)

def process_tiles(image: np.ndarray, boxes: list):
    """Returns a list of processed tile images, after trimming the edges and standardizing the array shape"""
    tile_images = []
    for box in boxes:
        tile_images.append(process_tile(image[box[1]:box[3],box[0]:box[2]]))
    return tile_images

tile_table = [Hands.Tile("", "nothing"),
              Hands.Tile("", "joker"),
              Hands.Tile("dot", "dragon"),
              Hands.Tile("bam", "dragon"),
              Hands.Tile("crak", "dragon"),
              Hands.Tile("", "flower"),
              Hands.Tile("wind", "north"),
              Hands.Tile("wind", "east"),
              Hands.Tile("wind", "west"),
              Hands.Tile("wind", "south"),
              Hands.Tile("bam", "1"),
              Hands.Tile("bam", "2"),
              Hands.Tile("bam", "3"),
              Hands.Tile("bam", "4"),
              Hands.Tile("bam", "5"),
              Hands.Tile("bam", "6"),
              Hands.Tile("bam", "7"),
              Hands.Tile("bam", "8"),
              Hands.Tile("bam", "9"),
              Hands.Tile("dot", "1"),
              Hands.Tile("dot", "2"),
              Hands.Tile("dot", "3"),
              Hands.Tile("dot", "4"),
              Hands.Tile("dot", "5"),
              Hands.Tile("dot", "6"),
              Hands.Tile("dot", "7"),
              Hands.Tile("dot", "8"),
              Hands.Tile("dot", "9"),
              Hands.Tile("crak", "1"),
              Hands.Tile("crak", "2"),
              Hands.Tile("crak", "3"),
              Hands.Tile("crak", "4"),
              Hands.Tile("crak", "5"),
              Hands.Tile("crak", "6"),
              Hands.Tile("crak", "7"),
              Hands.Tile("crak", "8"),
              Hands.Tile("crak", "9")]

base_tiles = [1,2,3,4,5,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,5,5,5,5,5,5,0]

standard_tiles = []

for i in range(43):
    standard_tiles.append(process_tile(cv.imread("images/SingleTiles/"+str(i)+".PNG", cv.IMREAD_REDUCED_GRAYSCALE_2)))
standard_tiles.append(standardize(cv.imread("images/SingleTiles/43.PNG", cv.IMREAD_REDUCED_GRAYSCALE_2)))
#Average height = 50.93023255813954
#Average width = 37.30232558139535

def identify_tile(tile: np.ndarray):
    """Returns the matching Tile object given a processed tile image"""
    #This is currently designed for rack tiles only, but should be easy to extend usage to other tiles by adjusting the size processing
    min_diff = np.sum(np.abs(standard_tiles[0] - tile))
    min_index = 0
    for i, standard_tile in enumerate(standard_tiles):
        cur_diff = np.sum(np.abs(standard_tile - tile))
        if cur_diff < min_diff:
            min_diff = cur_diff
            min_index = i
    return tile_table[base_tiles[min_index]]




b1_rack = [[29, 783, 162, 896], [164, 783, 295, 896], [295, 784, 428, 896], [429, 784, 560, 896], [562, 784, 694, 896], [693, 784, 825, 896], [827, 784, 960, 897], [960, 784, 1090, 897], [1092, 784, 1223, 896], [1225, 784, 1356, 896], [1357, 783, 1489, 896], [1489, 783, 1622, 896], [1622, 783, 1756, 896], [1753, 784, 1884, 896]]
reduced_rack = [[14, 391, 81, 448], [82, 391, 147, 448], [147, 392, 214, 448], [214, 392, 280, 448], [281, 392, 347, 448], [346, 392, 412, 448], [413, 392, 480, 448], [480, 392, 545, 448], [546, 392, 611, 448], [612, 392, 678, 448], [678, 391, 744, 448], [744, 391, 811, 448], [811, 391, 878, 448], [876, 392, 942, 448]]

t0 = time.time()
base_image = cv.imread("images/MultipleTiles/b1.PNG", cv.IMREAD_REDUCED_GRAYSCALE_2)
test_tiles = process_tiles(base_image, reduced_rack)
t1 = time.time()
labels = []
for test_tile in test_tiles:
    labels.append(identify_tile(test_tile))
t2 = time.time()
print("Processing time = " + str(t1 - t0))
print("Identification time = " + str(t2 - t1))
print("Total time = " + str(t2 - t0))
plt.ioff()
for i in np.arange(len(b1_rack)):
    cur_tile = b1_rack[i]
    print(labels[i])
    plt.imshow(test_tiles[i])
    plt.show()


