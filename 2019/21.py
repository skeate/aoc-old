from time import sleep
from random import shuffle
import heapq
import numpy as np
import os
import sys
import threading
from queue import Queue
from input21 import v
from icc import ICC

v = [int(x) for x in v.strip().split(',')]

iq = Queue()
oq = Queue()
icc = ICC(v, iq, oq)

def run(icc):
    icc.run()

t = threading.Thread(target=run, args=[icc])
t.start()

def show_output():
    l = '\n'
    while True:
        l = oq.get()
        if l > 255:
            print(l)
            break
        print(chr(l), end='')

t2 = threading.Thread(target=show_output)
t2.start()

def write_ascii(s):
    for c in s:
        iq.put(ord(c))
    iq.put(10)

# write_ascii('AND A T')
# write_ascii('NOT T T')
write_ascii('NOT A J')
write_ascii('NOT B T')
write_ascii('OR T J')
write_ascii('NOT C T')
write_ascii('OR T J')
write_ascii('AND D J')
write_ascii('WALK')
