# from keras.models import load_model
from colored_list import ColoredList
import numpy as np
from kafka import KafkaConsumer
from face_embedder import *
import time
import cv2
from PIL import Image
import msgpack
from utils import *
import json
from kafka_producer import KafkaProducer


def face_from_file(filename):
    img = cv2.imread(filename)
    return Face_Embedder.extract_face_from_mat(img)


face_will_1 = face_from_file("will.jpeg")
blist = ColoredList()
blist.add_face(face_will_1)

consumer = KafkaConsumer('frames', group_id='face_detection',
                         auto_offset_reset='largest')

producer = KafkaProducer()
thief_luck = 0
for record in consumer:
    thief_luck = (thief_luck + 1) % 5
    if thief_luck != 0:
        continue
    camera_id, time_stamp, image_str = record.value.decode().split('.')
    image = str_to_mat(image_str)
    cv2.imshow("Hello", image)
    cv2.waitKey(1)
    sent_face = Face_Embedder.extract_face_from_mat(image)
    if sent_face:
        print('found face')
        # use as black list
        if blist.search(sent_face) or True:
            to_send = ("%s, %s"%('Danger person', image_str)).encode()
            producer.send(to_send)
