from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont
import json
import Hands

client = genai.Client()

def parse_tile(label):
    label = label.lower()

    #Check for flowers or jokers
    if label.find("joker") != -1:
        return Hands.Tile("", "joker")
    if label.find("flower") != -1:
        return Hands.Tile("", "flower")

    #Check for tiles containing the word 'dragon'
    if label.find("dragon") != -1:
        dragons = ["red", "green", "white", "soap"]
        dragon_suits = ["crak", "bam", "dot", "dot"]
        for i, dragon in enumerate(dragons):
            if label.find(dragon) != -1:
                return Hands.Tile(dragon_suits[i], "dragon")

    #Check for tiles containing the word 'wind'
    if label.find("wind") != -1:
        directions = ["north", "east", "west", "south"]
        for direction in directions:
            if label.find(direction) != -1:
                return Hands.Tile("wind", direction)

    #Find the tile's suit
    suits = ["bam", "dot", "crak"]
    tile_suit = ""
    for suit in suits:
        if label.find(suit) != -1:
            tile_suit = suit
            break

    #Check for the value a wind/dragon tile where the label did not contain the word 'wind' or 'dragon'
    if tile_suit == "":
        match label:
            case "red" | "green" | "white" | "soap":
                dragons = ["red", "green", "white", "soap"]
                dragon_suits = ["crak", "bam", "dot", "dot"]
                return Hands.Tile(dragon_suits[dragons.index(label)], "dragon")
            case "north" | "east" | "west" | "south":
                return Hands.Tile("wind", label)
            case "n" | "e" | "w" | "s":
                winds = ["north", "east", "west", "south"]
                letters = ["n", "e", "w", "s"]
                return Hands.Tile("wind", winds[letters.index(label)])

    #Find value of bam/dot/crak tile
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for i, value in enumerate(values):
        if label.find(value) != -1:
            return Hands.Tile(tile_suit, values[i%9]) #Uses i%9 so that the numerical version of the values are used

    #If label does not match any of the previous conditions, raise an exception
    raise Exception("Hands.Tile parsing error with input: " + label)



def parse_json(json_output: str):
    # Parsing out the markdown fencing
    lines = json_output.splitlines()
    for i, line in enumerate(lines):
        if line == "```json":
            json_output = "\n".join(lines[i+1:])  # Remove everything before "```json"
            json_output = json_output.split("```")[0]  # Remove everything after the closing "```"
            break  # Exit the loop once "```json" is found
    return json_output

def identify_single_tile(path):
    prompt = ("Identify which American mahjong tile is visible in the image. Respond only with the name of the tile. " +
              "For bam/dot/crak tiles, use the format x suit, with x being the number and suit being bam, dot, or crak." +
              "Otherwise, just use the name of the tile as it appears here: (joker, flower, red, green, white, north wind, east wind, west wind, south wind).")
    image = Image.open(path)
    config = types.GenerateContentConfig(
        response_mime_type = "application/json",
        thinking_config=types.ThinkingConfig(thinking_budget=1024)
    )
    response = client.models.generate_content(model="gemini-2.5-flash",
                                              contents=[image, prompt],
                                              config=config)
    return parse_json(response.text)
def identify_multiple_tiles(path):
    prompt = ("Identify which specific American mahjong tiles are visible in the image, and their bounding boxes. " +
              "The box_2d should be [ymin, xmin, ymax, xmax] normalized to 0-1000. " +
              "Labels should be the exact American mahjong tile, with suits bam, crak, and dot. " +
              "REMEMBER THAT 1 BAM LOOKS VERY SIMILAR TO FLOWERS. 1 BAM DEPICTS A BIRD.")
    image = Image.open(path)
    config = types.GenerateContentConfig(
        response_mime_type = "application/json",
        thinking_config=types.ThinkingConfig(thinking_budget=1024)
    )
    response = client.models.generate_content(model="gemini-2.5-flash",
                                              contents=[image, prompt],
                                              config=config)
    return parse_json(response.text)

def locate_multiple_tiles(path):
    prompt = "Give the bounding boxes of the single mahjong tiles in this image as a JSON array. The box_2d should be [ymin, xmin, ymax, xmax] normalized to 0-1000. NEVER GROUP MORE THAN 1 TILE TOGETHER."
    image = Image.open(path)
    config = types.GenerateContentConfig(
        response_mime_type = "application/json",
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
    response = client.models.generate_content(model="gemini-2.5-flash",
                                              contents=[image, prompt],
                                              config=config)
    return parse_json(response.text)


def plot_bounding_boxes(img_path, bounding_boxes):
    """
    Plots bounding boxes on an image with markers for each a name, using PIL, normalized coordinates, and different colors.

    Args:
        img_path: The path to the image file.
        bounding_boxes: A list of bounding boxes containing the name of the object
         and their positions in normalized [y1 x1 y2 x2] format.
    """

    # Load the image
    img = Image.open(img_path)
    width, height = img.size

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", size=20)

    # Iterate over the bounding boxes
    for bounding_box in json.loads(bounding_boxes):
        color = 'black'

        # Convert normalized coordinates to absolute coordinates
        abs_y1 = int(bounding_box["box_2d"][0]/1000 * height)
        abs_x1 = int(bounding_box["box_2d"][1]/1000 * width)
        abs_y2 = int(bounding_box["box_2d"][2]/1000 * height)
        abs_x2 = int(bounding_box["box_2d"][3]/1000 * width)

        if abs_x1 > abs_x2:
            abs_x1, abs_x2 = abs_x2, abs_x1

        if abs_y1 > abs_y2:
            abs_y1, abs_y2 = abs_y2, abs_y1

        # Draw the bounding box
        draw.rectangle(
            ((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=4
        )

        # Draw the text
        if "label" in bounding_box:
            draw.text((abs_x1 + 8, abs_y2 - 25), bounding_box["label"], fill=color, font=font)

    # Display the image
    img.show()

def get_tiles(bounding_boxes):
    tiles = []
    for tile in json.loads(bounding_boxes):
        label = tile["label"]
        tiles.append(parse_tile(label))
    return tiles



testPath = "images/MultipleTiles/o.PNG"
boxes = identify_multiple_tiles(testPath)
testTiles = get_tiles(boxes)
print("Rack:")
for testTile in testTiles:
    print(str(testTile) + ", ", end='')
print("\nBest Hands:")
top_hands = Hands.find_closest_hands(Hands.sort_hand(testTiles), 3)
print(top_hands)