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

def w(s):
    for c in s:
        iq.put(ord(c))
    iq.put(10)


w('NOT B T')
w('OR T J')
w('NOT C T')
w('OR T J')

w('OR J T')
w('AND H T')
w('AND T J')

w('AND D J')
w('NOT A T')
w('OR T J')
w('RUN')


# .................
# .................
# ..@..............
# #####.#.#...#####
#    ABCDEFGHI
