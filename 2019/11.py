import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import threading
from queue import Queue
from input11 import v
from icc import ICC
from grid import Grid

v = [int(x) for x in v.strip().split(',')]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def noop(g, l): pass

def paint_start(color):
    iq = Queue()
    oq = Queue()
    cc = ICC(v, iq, oq)

    dr = UP
    loc = (0, 0)

    panels = Grid(noop)

    running = True

    def paint_grid():
        nonlocal loc, dr
        while running:
            panels.grid[loc] = oq.get() # color
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
            if loc in panels.grid:
                iq.put(panels.grid[loc])
            else:
                iq.put(0)

    t = threading.Thread(target=paint_grid)
    t.start()

    iq.put(color)
    cc.run()

    running = False
    t.join()

    return panels

print(len(paint_start(0).grid))

paint_start(1).display(
    flipy=True,
    trans=lambda x: ' ' if x == 0 else '#'
)
