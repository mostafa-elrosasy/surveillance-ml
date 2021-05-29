import cv2
import base64
import numpy as np
from time import sleep
import cv2
import base64
import datetime
import json
from face_embedder import *


def forgiving_json_deserializer(v):
    if v is None:
        return
    try:
        return json.loads(v.decode('utf-8'))
    except:
        return None


def make_message(camera_id, time_stamp, data):
    return {
        "camera_id": camera_id,
        "time_stamp": time_stamp,
        "image": data
    }

def mat_to_str(image):
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text


def str_to_mat(im_b64):
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def time(fun):
    print("*********************************")
    start_time = time.time()
    fun()
    print("--- %s seconds ---" % (time.time() - start_time))
    print("*********************************")



# consumer = KafkaConsumer('frames', group_id='face_detection',
#                      value_deserializer=forgiving_json_deserializer,
#                      auto_offset_reset='earliest')
