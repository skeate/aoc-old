from time import sleep
from random import shuffle
import heapq
import numpy as np
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from grid import Grid
import threading
from queue import Queue
from input19 import v
from icc import ICC

v = [int(x) for x in v.strip().split(',')]

iq = Queue()
oq = Queue()
icc = ICC(v, iq, oq)

def run(icc):
    icc.run(continuous=True)

t = threading.Thread(target=run, args=[icc])
t.start()

g = np.ndarray((50,50), dtype=int)
for y in range(50):
    for x in range(50):
        iq.put(x)
        iq.put(y)
        g[y][x] = oq.get()

print(np.sum(g))

def corners(c):
    x,y = c
    iq.put(x)
    iq.put(y)
    iq.put(x + 99)
    iq.put(y)
    iq.put(x)
    iq.put(y + 99)
    return {'ul': oq.get(), 'ur': oq.get(), 'll': oq.get()}

def valid_box(p):
    return all(x == 1 for x in corners(p).values())

def shift(p, mode):
    if mode == 'left':
        return (p[0] - 1, p[1])
    elif mode == 'up':
        return  (p[0], p[1] - 1)
    return (p[0] - 1, p[1] - 1)

def find_from(p):
    l = shift(p, 'left')
    if valid_box(l):
        return find_from(l)
    u = shift(p, 'up')
    if valid_box(u):
        return find_from(u)
    b = shift(p, 'both')
    if valid_box(b):
        return find_from(b)
    uul = shift(u, 'both')
    if valid_box(uul):
        return find_from(uul)
    return p


slope_a = -49 / np.min(np.argwhere(g[49] == 1))
slope_b = -49 / np.max(np.argwhere(g[49] == 1))
between = (slope_b - slope_a) / 2 + slope_a

def approx_width_at_row(r):
    return -r * (1/slope_b - 1/slope_a)

approx_start = -100 // slope_a
target = 100 + approx_start
r = 50
while approx_width_at_row(r) < target:
    r += 1

approx_area = (-r // between - 25, r)

found = find_from(approx_area)
print(int(found[0] * 10000 + found[1]))
