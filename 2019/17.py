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
from input17 import v
from icc import ICC

v = [int(x) for x in v.strip().split(',')]

iq = Queue()
oq = Queue()
icc = ICC(v, iq, oq)

def run(icc):
    icc.run()

t = threading.Thread(target=run, args=[icc])
t.start()

def get_feed():
    s=''
    p = None
    n = oq.get()
    if n > 127:
        return n
    while n!=10 or p!=10:
        s += chr(n)
        p = n
        n = oq.get()
    return s

scaffolds = get_feed().strip().split('\n')
nscaffolds = np.ndarray((len(scaffolds), len(scaffolds[0])),dtype=int)
for y, r in enumerate(scaffolds):
    nscaffolds[y] = [ord(c) for c in r]
start = None
for y, r in enumerate(scaffolds):
    for x, c in enumerate(r):
        if c in '^<>v':
            start = (x, y)
            break


find = np.array([
    [ord(x) for x in '.#.'],
    [ord(x) for x in '###'],
    [ord(x) for x in '.#.'],
])

intersections = set()
for y in range(len(nscaffolds) - 2):
    for x in range(len(nscaffolds[y]) - 2):
        if np.all(nscaffolds[y:y+3, x:x+3] == find):
            intersections.add((x+1,y+1))

print(sum(a*b for a,b in intersections))
t.join()

# part 2
v[0] = 2

iq = Queue()
oq = Queue()
icc = ICC(v, iq, oq)

t = threading.Thread(target=run, args=[icc])
t.start()

def send_str(s):
    if len(s) > 20:
        print(f'{s} > 20 chars')
    for c in s:
        iq.put(ord(c))
    iq.put(ord('\n'))

full_seq = '''
L,12,L,10,R,8,L,12,
R,8,R,10,R,12,
L,12,L,10,R,8,L,12,
R,8,R,10,R,12,
L,10,R,12,R,8,
L,10,R,12,R,8,
R,8,R,10,R,12,
L,12,L,10,R,8,L,12,
R,8,R,10,R,12,
L,10,R,12,R,8
'''

# allowed memory:
#         12345678901234567890
send_str('A,B,A,B,C,C,B,A,B,C')
send_str('L,12,L,10,R,8,L,12')
send_str('R,8,R,10,R,12')
send_str('L,10,R,12,R,8')
enable_playback = False
send_str('y' if enable_playback else 'n')

if enable_playback:
    while True:
        f = get_feed()
        os.system('clear')
        print(f)
        if type(f) is int:
            break
else:
    get_feed()
    get_feed()
    get_feed()
    print(oq.get())
