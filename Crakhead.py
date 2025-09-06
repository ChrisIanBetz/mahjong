from pathlib import Path
import time
from PIL import Image, ImageFont, ImageDraw
import RoboflowBoxes
from ManualTile import *
# import cv2 as cv
# import matplotlib.pyplot as plt
# from Hands import *

def label_sort(box):
    return box["label"]

def plot_bounding_boxes(img_path: str, bounding_boxes: list):
    """
    Plots bounding boxes on an image with markers for each a name, using PIL, normalized coordinates, and different colors.

    Args:
        img_path: The path to the image file.
        bounding_boxes: A list of bounding boxes containing the name of the object
         and their positions in normalized [x1 y1 x2 y2] format.
    """

    # Load the image
    img = Image.open(img_path)
    width, height = img.size

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", size=20)

    bounding_boxes.sort(key=label_sort)
    index = 0
    # Iterate over the bounding boxes
    for bounding_box in bounding_boxes:
        match index:
            case 0:
                color = 'black'
                weight = 10
            case 1:
                color = 'red'
                weight = 10
            case 2:
                color = 'orangered'
                weight = 10
            case _:
                color = 'gray'
                weight = 6
        #color = 'gray'


        # Convert normalized coordinates to absolute coordinates
        abs_x1 = int(bounding_box["box_2d"][0])
        abs_y1 = int(bounding_box["box_2d"][1])
        abs_x2 = int(bounding_box["box_2d"][2])
        abs_y2 = int(bounding_box["box_2d"][3])

        if abs_x1 > abs_x2:
            abs_x1, abs_x2 = abs_x2, abs_x1

        if abs_y1 > abs_y2:
            abs_y1, abs_y2 = abs_y2, abs_y1

        # Draw the bounding box
        draw.rectangle(
            ((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=weight
        )

        # Draw the text
        if "label" in bounding_box:
            text_box = draw.textbbox((abs_x1 + 8, abs_y1 - 25), bounding_box["label"], font=font)
            draw.rectangle(text_box, fill='white')
            draw.text((abs_x1 + 8, abs_y1 - 25), bounding_box["label"], fill=color, font=font)

        index += 1

    # Display the image
    img.show()
    return img

def full_rundown(img_path: str, tiles: [Hands.Tile], boxes: list, show_depth=1, depth=2):
    print("\n\n-----Full Rundown-----\n")
    print("Rack:")
    for tile in tiles[0:len(tiles)-1]:
        print(str(tile) + ", ", end='')
    print(str(tiles[len(tiles)-1]))

    top_hands, top_discards = Hands.find_closest_hands(tiles, show_depth, depth)

    index = 0
    labeled_boxes = []
    for box in boxes:
        labeled_boxes.append({'label': str(top_discards[index]['strength rating']), 'box_2d': box})
        index += 1
    image = plot_bounding_boxes(img_path, labeled_boxes)
    #image.close()

    top_discards.sort(order='strength rating')
    print("\nBest Discards: (depth = " + str(depth) + ")")
    for entry in top_discards:
        print(str(entry['tile']) + " --> strength = " + str(entry['strength rating']))

    print("\nBest Hands:")
    for hand in top_hands:
        print(str(hand['hand']) + " - " + str(hand['distance']) + " tiles away")

path = Path("Screenshots")

def get_newest():
    """Returns the path string of the most recent screenshot"""
    path_list = list(path.iterdir())
    newest = -1
    for p in path_list[1:]:
        s = str(p)
        num = int(s[s.index("(")+1:s.index(")")])
        newest = max(newest, num)
    return "Screenshots\\Screenshot (" + str(newest) + ").png"

def clear():
    """Deletes all screenshots from the directory"""
    path_list = list(path.iterdir())
    for p in path_list[1:]:
        if str(p).endswith(".png"):
            p.unlink()

def setup() -> (str, list):
    clear()
    while len(list(path.iterdir())) < 2:
        print("Waiting for screenshot...")
        time.sleep(1)
    print("Locating rack...")
    image_path = get_newest()
    return image_path, RoboflowBoxes.get_rack_boxes(image_path)

def run():
    newest_path, rack_boxes = setup()
    t0 = time.time()
    rack_tiles = identify_tiles(process_tiles(read_image(newest_path), rack_boxes))
    t1 = time.time()
    print("Identification time = " + str(t1 - t0))
    full_rundown(newest_path, rack_tiles, rack_boxes)
    print("Analysis time = " + str(time.time() - t1))
    running = True
    size = len(list(path.iterdir()))
    while running:
        path_list = list(path.iterdir())
        if len(path_list) > size:
            size = len(path_list)
            newest_path = get_newest()
            t0 = time.time()
            rack_tiles = identify_tiles(process_tiles(read_image(newest_path), rack_boxes))
            t1 = time.time()
            print("Identification time = " + str(t1 - t0))
            full_rundown(newest_path, rack_tiles, rack_boxes)
            print("Analysis time = " + str(time.time() - t1))

        if len(path_list) > 100:
            running = False
        time.sleep(1)
    clear()


run()
clear()
