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


def update_bad_faces_count(cnt):
    print("bad faces: " + str(cnt))
    file = open('danger_faces_count.out', 'w')
    file.write('%s\n'%(str(cnt)))
    file.close()

def update_unique_faces_count(cnt):
    file = open('unique_faces_count.out', 'w')
    file.write('%s\n'%(str(cnt)))
    file.close()

def faces_from_file(filename):
    img = cv2.imread(filename)
    return Face_Embedder.extract_faces_from_mat(img)

timer = Timer()

blist = ColoredList()

faces_files = ["pacino1.jpg", "pacino2.jpg", "cazale1.jpg"]
for file in faces_files:
    face = faces_from_file(file)[0]
    face.setID(file[0:3])
    blist.add_face(face)

consumer = KafkaConsumer('frames', group_id='face_detection', auto_offset_reset='largest')
# consumer = KafkaConsumer('frames', group_id='face_detection')

producer = KafkaProducer()
thief_luck = 0
bad_faces_set = set()
good_faces = ColoredList()
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
        match, dist, id = blist.search(sent_face)
        print('found face: ' + str(dist))
        if match:
            found = True
            bad_faces_set.add(id)
            print('and matched')
            draw_bounding_box(image, *sent_face.dims, "Danger person")
        else:
            match, dist, id = good_faces.search(sent_face)
            if not match:
                good_faces.add_face(sent_face)


    if found:
        timer.mark_time()
        image_str = mat_to_str(image)
        to_send = ("%s,%s,%s"%('Danger person', image_str.decode(), dist)).encode()
        producer.send(to_send)
    update_unique_faces_count(len(good_faces.faces) + len(bad_faces_set))
    update_bad_faces_count(len(bad_faces_set))