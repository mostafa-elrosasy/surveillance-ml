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
from timer import Timer


def faces_from_file(filename):
    img = cv2.imread(filename)
    return Face_Embedder.extract_faces_from_mat(img)

timer = Timer()

blist = ColoredList()

faces_files = ["will.jpeg", "leo1.jpg", "judi1.jpg", "foster1.jpg", "pacino1.jpg", "pacino2.jpg", "cazale1.jpg"]
for file in faces_files:
    face = faces_from_file(file)[0]
    blist.add_face(face)

consumer = KafkaConsumer('frames', group_id='face_detection', auto_offset_reset='largest')
# consumer = KafkaConsumer('frames', group_id='face_detection')

producer = KafkaProducer()
thief_luck = 0
for record in consumer:
    thief_luck = (thief_luck + 1) % 3
    if thief_luck != 0:
        continue
    if not timer.its_time():
        continue
    camera_id, time_stamp, image_str = record.value.decode().split('.')
    image = str_to_mat(image_str)
    cv2.imshow("Hello", image)
    cv2.waitKey(1)
    faces = Face_Embedder.extract_faces_from_mat(image)
    found = False
    for sent_face in faces:
        # use as black list
        match, dist = blist.search(sent_face)
        print('found face: ' + str(dist))
        if match:
            found = True
            print('and matched')
            draw_bounding_box(image, *sent_face.dims, "Danger person")
    if found:
        timer.mark_time()
        image_str = mat_to_str(image)
        to_send = ("%s,%s,%s"%('Danger person', image_str.decode(), dist)).encode()
        producer.send(to_send)
