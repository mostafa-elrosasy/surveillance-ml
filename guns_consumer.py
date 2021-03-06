from kafka import KafkaConsumer
import cv2
from kafka_producer import KafkaProducer
import numpy as np
import base64
from guns import detector
from timer import Timer
from utils import mat_to_str, str_to_mat

def update_gun_count(cnt):
    file = open('guns_count.out', 'w')
    file.write('%s\n'%(str(cnt)))
    file.close()

consumer = KafkaConsumer('frames', group_id='gun_detection',
                         auto_offset_reset='largest')

producer = KafkaProducer()

timer = Timer()

detector = detector()
counter = 0
for record in consumer:
    if not timer.its_time():
        continue
    camera_id, time_stamp, image_str = record.value.decode().split('.')
    image = str_to_mat(image_str)
    image, detection, conf = detector.process(image)
    if detection:
        timer.mark_time()
        print("GUN detected")
        image_str = mat_to_str(image)
        to_send = ("%s,%s,%s"%('GUN detected', image_str.decode(), conf))
        producer.send(to_send.encode())
        # cv2.imwrite("outputs/object-detection%s.jpg" % counter, image)
        counter += 1
        update_gun_count(counter)