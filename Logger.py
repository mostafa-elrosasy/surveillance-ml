from kafka import KafkaConsumer
import time
import base64
import cv2

from utils import str_to_mat
from notify import *

THRESHHOLD = 5
last_print = dict()
def write_image(img, name):
    img = str_to_mat(img.encode())
    cv2.imwrite(name, img)


def append_to_file(msg, img, conf):
    if msg not in last_print or time.time() - last_print[msg] > THRESHHOLD:
        t = time.time()
        img_name = "log_img/" + str(int(t * 10)) + '.jpg'
        write_image(img, img_name)
        file = open('log.out', 'a')
        file.write('%s,%s,%s,%s\n'%(t, msg, img_name, conf))
        file.close()
        # send_notification(msg)
        last_print[msg] = t
        print("Done a log")


# consumer = KafkaConsumer('notification', auto_offset_reset='earliest')
consumer = KafkaConsumer('notification')

for record in consumer:
    arr = record.value.decode().split(',')
    print("message: " + arr[0])
    append_to_file(arr[0], arr[1], arr[2])
