from kafka import KafkaConsumer
import time


THRESHHOLD = 15
last_print = dict()
def append_to_file(msg, img):
    if msg not in last_print or time.time() - last_print[msg] > THRESHHOLD:
        t = time.time()
        file = open('log.out', 'a')
        file.write('%s, %s, %s\n'%(t, msg, img))
        file.close()
        last_print[msg] = t


consumer = KafkaConsumer('notification',
                         auto_offset_reset='largest')

for record in consumer:
    arr = record.value.decode().split(',')
    append_to_file(arr[0], arr[1])

    # TODO: send notification
