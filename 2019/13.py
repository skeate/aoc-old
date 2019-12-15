from time import sleep
from curses import wrapper
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import threading
from queue import Queue
from input13 import v
from icc import ICC
from grid import Grid

v = [int(x) for x in v.strip().split(',')]

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def noop(g, l): pass

iq = Queue()
oq = Queue()
cc = ICC(v, iq, oq)
tiles = Grid(noop)
cc.run()
while not oq.empty():
    x = oq.get()
    y = oq.get()
    tid = oq.get()
    tiles.grid[(x,y)] = tid

print(len([c for c,t in tiles.grid.items() if t == 2]))

v[0] = 2

iq = Queue()
oq = Queue()
oq.put(0)
oq.put(0)
oq.put(0)
cc = ICC(v, iq, oq)
score = 0

def draw_tile(t):
    char = ' '
    color = 37
    if t == WALL:
        char = '\u2593'
    elif t == BLOCK:
        color = 34
        char = '\u2588'
    elif t == PADDLE:
        color = 35
        char = '\u2594'
    elif t == BALL:
        color = 31
        char = 'o'
    return f'\u001b[{color}m{char}\u001b[0m'

running = True
def play():
    global iq, oq, score, running

    tiles = Grid(noop)
    sleep(.2)
    while running:
        while not oq.empty():
            x = oq.get()
            y = oq.get()
            tid = oq.get()
            if x == -1 and y == 0:
                score = tid
            else:
                tiles.grid[(x,y)] = tid

        ballx = [c[0] for c,v in tiles.grid.items() if v == BALL][0]
        paddlex = [c[0] for c,v in tiles.grid.items() if v == PADDLE][0]
        if ballx < paddlex:
            iq.put(-1)
        elif ballx > paddlex:
            iq.put(1)
        else:
            iq.put(0)
        os.system('clear')
        tiles.display(trans=draw_tile)
        sleep(.01)
    while not oq.empty():
        x = oq.get()
        y = oq.get()
        tid = oq.get()
        if x == -1 and y == 0:
            score = tid
        else:
            tiles.grid[(x,y)] = tid


t = threading.Thread(target=play)
t.start()
tiles = Grid(noop)
cc.run()
running = False
t.join()
print(score)
