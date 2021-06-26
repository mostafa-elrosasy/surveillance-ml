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


blist = ColoredList()
faces_files = ["will.jpeg", "leo1.jpg", "judi1.jpg", "foster1.jpg", "pacino1.jpg", "pacino2.jpg"]
for file in faces_files:
    face = face_from_file(file)
    blist.add_face(face)

consumer = KafkaConsumer('frames', group_id='face_detection', auto_offset_reset='largest')
# consumer = KafkaConsumer('frames', group_id='face_detection')

producer = KafkaProducer()
thief_luck = 0
for record in consumer:
    thief_luck = (thief_luck + 1) % 5
    camera_id, time_stamp, image_str = record.value.decode().split('.')
    image = str_to_mat(image_str)
    cv2.imshow("Hello", image)
    cv2.waitKey(1)
    sent_face = Face_Embedder.extract_face_from_mat(image)
    if sent_face:
        # use as black list
        match, dist = blist.search(sent_face)
        print('found face: ' + str(dist))
        if match:
            print('and matched')
            draw_bounding_box(image, *sent_face.dims, "Danger person")
            image_str = mat_to_str(image)
            to_send = ("%s,%s,%s"%('Danger person', image_str.decode(), dist)).encode()
            producer.send(to_send)
