#import time
from inference import get_model
import supervision as sv
import cv2 as cv
import numpy as np
#import matplotlib.pyplot as plt


#Load roboflow model
model = get_model(model_id="mahjong-pdpfj/2")

def plot_boxes(path):
    image = cv.imread(path)
    results = model.infer(image)[0]
    print(results)
    detections = sv.Detections.from_inference(results)
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    sv.plot_image(annotated_image)

def x_value(box: list):
    return box[0] #For sorting xyxy bounding box predictions by x value
def y_value(box):
    return box.y #For sorting xywh bounding box predictions by y value

def convert_xywh_to_xyxy(box):
    x1 = int(box.x - (box.width / 2))
    y1 = int(box.y - (box.height / 2))
    x2 = int(box.x + (box.width / 2))
    y2 = int(box.y + (box.height / 2))
    return [x1, y1, x2, y2]

def get_boxes(path):
    image = cv.imread(path)
    results = model.infer(image)[0]
    detections = sv.Detections.from_inference(results)
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    sv.plot_image(annotated_image)
    preds = results.predictions
    boxes = []
    for pred in preds:
        boxes.append(convert_xywh_to_xyxy(pred))
    return boxes

def get_rack_boxes(path):
    #Establish the bounding boxes of the player's rack
    #This slow function should only be called once per game at the beginning
    #FUNCTION WILL NOT WORK IF CALLED ON A GAME STATE WITH CALLED TILES

    image = cv.imread(path)
    boxes = model.infer(image)[0].predictions #Get bounding boxes of full image
    boxes.sort(key=y_value, reverse=True)

    rack = []
    average_y = 0
    average_width = 0
    average_height = 0
    for i in np.arange(13): #Append lowest 13 tiles to rack
        box = boxes[i]
        rack.append(convert_xywh_to_xyxy(box))
        average_y += box.y / 13
        average_width += box.width / 13
        average_height += box.height / 13

    if len(boxes) >= 14 and abs(boxes[13].y - average_y) < 25: #Check if rack contains 14 tiles
        rack.append(convert_xywh_to_xyxy(boxes[13])) #If so, append the 14th tile
        rack.sort(key=x_value)
    else:
        rack.sort(key=x_value) #If not, extrapolate where the 14th tile should go
        x1 = int(rack[12][0] + average_width)
        x2 = int(x1 + average_width)
        y1 = int(average_y - (average_height / 2))
        y2 = int(average_y + (average_height / 2))
        rack.append([x1, y1, x2, y2])
    return rack

test_path = "images/MultipleTiles/y.PNG"

print(get_boxes(test_path))

#test_image = cv.imread(test_path)
# rack_boxes = get_rack_boxes(test_path)
# print(rack_boxes)





