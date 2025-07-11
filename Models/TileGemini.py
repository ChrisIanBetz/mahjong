from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont, ImageColor
import json

class Tile:
    #Suit - (bam, dot, crak, dragon, wind, flower, joker)
    #Value - (1-9 for bam/dot/crak, 0 otherwise)
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


client = genai.Client()
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
    return response.text
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
    return response.text

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
    #bounding_boxes = json.loads(response.text)
    return response.text

def parse_json(json_output: str):
    # Parsing out the markdown fencing
    lines = json_output.splitlines()
    for i, line in enumerate(lines):
        if line == "```json":
            json_output = "\n".join(lines[i+1:])  # Remove everything before "```json"
            json_output = json_output.split("```")[0]  # Remove everything after the closing "```"
            break  # Exit the loop once "```json" is found
    return json_output

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
    print(img.size)
    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Parsing out the markdown fencing
    bounding_boxes = parse_json(bounding_boxes)

    font = ImageFont.truetype("arial.ttf", size=20)

    # Iterate over the bounding boxes
    for i, bounding_box in enumerate(json.loads(bounding_boxes)):
        # Select a color from the list
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

testPath = "../images/MultipleTiles/o.PNG"
boxes = identify_multiple_tiles(testPath)
plot_bounding_boxes(testPath, boxes)