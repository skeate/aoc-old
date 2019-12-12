import threading
from queue import Queue
from input11 import v
from icc import ICC
from grid import Grid

v = [int(x) for x in v.strip().split(',')]

iq = Queue()
oq = Queue()
cc = ICC(v, iq, oq)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
dr = UP
loc = (0, 0)

panels = {}

running = True

def paint_grid():
    global panels, dr, loc, cc, running
    while running:
        panels[loc] = oq.get() # color
        turn = oq.get()
        dr = ((turn * 2 - 1) + dr) % 4
        if dr == UP:
            loc = (loc[0], loc[1] + 1)
        elif dr == LEFT:
            loc = (loc[0] - 1, loc[1])
        elif dr == RIGHT:
            loc = (loc[0] + 1, loc[1])
        elif dr == DOWN:
            loc = (loc[0], loc[1] - 1)
        if loc in panels:
            iq.put(panels[loc])
        else:
            iq.put(0)

t = threading.Thread(target=paint_grid)
t.start()

iq.put(1)
cc.run()

running = False
t.join()

print(len(panels))

minx = min(x[0] for x in panels.keys())
miny = min(x[1] for x in panels.keys())
maxx = max(x[0] for x in panels.keys())
maxy = max(x[1] for x in panels.keys())

for y in reversed(range(miny, maxy + 1)):
    for x in range(minx, maxx + 1):
        if (x,y) in panels and panels[(x,y)] == 1:
            print('#', end='')
        else:
            print(' ', end='')
    print()
