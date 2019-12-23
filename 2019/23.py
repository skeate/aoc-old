from time import sleep
from random import shuffle
import heapq
import numpy as np
import os
import sys
import threading
from queue import Queue
from input23 import v
from icc import ICC

v = [int(x) for x in v.strip().split(',')]

def run(icc):
    icc.run()

natx = None
naty = None
ts = []

def manager(s, oq):
    global natx, naty
    found = False
    while len(ts) < 50:
        sleep(.01)
    while True:
        target = oq.get()
        x = oq.get()
        y = oq.get()
        if target == 255:
            if not found:
                print('255:',y)
                found = True
            natx = x
            naty = y
        else:
            # print(f'{s:3d} -> {target:3d}: {x} \t {y}')
            if 0 <= target < 50:
                ts[target][1].put(x)
                ts[target][1].put(y)

for x in range(50):
    iq = Queue()
    iq.put(x)
    oq = Queue()
    icc = ICC(v, iq, oq, id=x, default_input=-1)
    t = threading.Thread(target=run, args=[icc])
    t.start()
    ts.append((t, iq, oq))
    m = threading.Thread(target=manager, args=[x, oq])
    m.start()

def nat():
    global natx, naty
    last_y = None
    sleep(1)
    while True:
        while natx is None or naty is None or not all(t[1].empty() and t[2].empty() for t in ts):
            sleep(0.01)
        if last_y is not None and naty == last_y:
            print('repeated: ', naty)
        last_y = naty
        ts[0][1].put(natx)
        ts[0][1].put(naty)
        natx = None
        naty = None

n = threading.Thread(target=nat)
n.start()
