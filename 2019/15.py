from time import sleep
from random import shuffle
import heapq
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from grid import Grid
import threading
from queue import Queue
from input15 import v
from icc import ICC

v = [int(x) for x in v.strip().split(',')]

iq = Queue()
oq = Queue()
icc = ICC(v, iq, oq)

def run():
    icc.run()

t = threading.Thread(target=run)
t.start()

WALL = '\u2588'
SPACE = '\u2591'
OXYGEN = '\u2573'

U = 1
D = 2
L = 3
R = 4

def reverse(m):
    if m % 2 == 0:
        return m - 1
    return m + 1

def manhattan(start, end):
    dx = abs(start[0] - end[0])
    dy = abs(start[1] - end[1])
    return dx + dy

def neighbors(p):
    x,y = p
    ns = [((x, y+1), U), ((x, y-1), D), ((x - 1, y), L), ((x + 1, y), R)]
    shuffle(ns)
    return ns

def astar(start, end, maze):
    pq = []
    heapq.heappush(pq, (manhattan(start, end), start, []))
    visited = set()
    while len(pq) > 0:
        dist, n, path = heapq.heappop(pq)
        if n == end:
            return path
        visited.add(n)
        nbs = neighbors(n)
        for nb, d in nbs:
            if nb not in visited and nb in maze and maze[nb] != WALL:
                heapq.heappush(pq, (manhattan(nb, end), nb, path + [d]))

def move(p, dp):
    return (p[0] + dp[0], p[1] + dp[1])


maze = {(0,0): 'o', (-10, 20): ' ', (5, -5): ' '}
g = Grid()
g.grid = maze

oxygen_loc = None

def explore(maze, loc, path = []):
    global oxygen_loc
    # os.system('clear')
    # g.display(flipy=True, mark=loc)
    # sleep(.01)
    for nb, d in neighbors(loc):
        if nb not in maze:
            iq.put(d)
            tile = oq.get()
            # print(nb, tile)
            if tile == 0:
                maze[nb] = WALL
            elif tile == 1:
                maze[nb] = SPACE
            elif tile == 2:
                maze[nb] = OXYGEN
                oxygen_loc = nb
            if maze[nb] != WALL:
                explore(maze, nb, path + [d])
                iq.put(reverse(d))
                oq.get()

explore(maze, (0,0))
print(len(astar((0,0), oxygen_loc, maze)))

def fill_from(locs, maze, steps=0):
    # os.system('clear')
    # g.display(flipy=True)
    # sleep(.01)
    nlocs = []
    for loc in locs:
        for nb, d in neighbors(loc):
            if nb in maze and maze[nb] == SPACE:
                nlocs.append(nb)
                maze[nb] = OXYGEN
    if len(nlocs) > 0:
        steps = fill_from(nlocs, maze, steps + 1)
    return steps


print(fill_from([oxygen_loc], maze))
