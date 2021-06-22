from kafka import KafkaConsumer
import cv2
from kafka_producer import KafkaProducer
import numpy as np
import base64
from guns import detector
import time
from utils import str_to_mat

consumer = KafkaConsumer('frames', group_id='gun_detection',
                         auto_offset_reset='largest')

producer = KafkaProducer()

detector = detector()
counter = 1
for record in consumer:
    camera_id, time_stamp, image_str = record.value.decode().split('.')
    image = str_to_mat(image_str)
    image, detection = detector.process(image)
    if detection:
        to_send = ("%s, %s"%('GUN detected', image_str))
        producer.send(to_send)
        cv2.imwrite("outputs/object-detection%s.jpg" % counter, image)
        # log here
    counter += 1