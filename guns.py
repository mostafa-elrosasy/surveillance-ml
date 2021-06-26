from threading import Condition
import cv2
import argparse
import numpy as np
from utils import draw_bounding_box

class detector:
    net = cv2.dnn.readNet("./darknet/yolov3_custom_train_last.weights",
                          "./darknet/cfg/yolov3_custom_train.cfg")

    # function to get the output layer names 
    # in the architecture
    def get_output_layers(self, net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers


    # read input image

    # read pre-trained model and config file
    def process(self, image):
         
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392
        # create input blob 
        blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
        # set input blob for the network
        self.net.setInput(blob)
        # run inference through the network
        # and gather predictions from output layers
        outs = self.net.forward(self.get_output_layers(self.net))
        # initialization
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.7
        nms_threshold = 0.4
        # for each detetion from each output layer 
        # get the confidence, class id, bounding box params
        # and ignore weak detections (confidence < 0.5)
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        # apply non-max suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        # go through the detections remaining
        # after nms and draw bounding box
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            draw_bounding_box(image, round(x), round(y), round(x+w), round(y+h), "Gun")
        return image, len(indices) != 0, max(confidences) if confidences else 0
