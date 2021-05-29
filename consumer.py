from kafka import KafkaConsumer
import cv2
import numpy as np
import base64
from guns import detector
import time

consumer = KafkaConsumer('frames', group_id='gun_detection',
                         auto_offset_reset='earliest')
detector = detector()
counter = 1
for record in consumer:
    camera_id, time_stamp, image_str = record.value.decode().split('.')
    image = str_to_mat(image_str)
    detection = detector.process(image)
    cv2.imwrite("outputs/object-detection%s.jpg" % counter, detection)
    counter += 1