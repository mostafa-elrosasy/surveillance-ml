import time

file = open('log.out', 'a')
THRESHHOLD = 30
last_print = dict()
def append(src, msg):
    if src not in last_print or time.time() - last_print[src] > THRESHHOLD:
        t = time.time()
        file.write('%s: %s'%(t, msg))
        last_print[src] = t