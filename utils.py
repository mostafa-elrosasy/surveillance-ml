import cv2
import base64
import numpy as np
from time import sleep
import cv2
import base64
import datetime
import json


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




# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, x, y, x_plus_w, y_plus_h, msg):
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), (255, 0, 0), 2)
    cv2.putText(img, msg, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


# consumer = KafkaConsumer('frames', group_id='face_detection',
#                      value_deserializer=forgiving_json_deserializer,
#                      auto_offset_reset='earliest')
