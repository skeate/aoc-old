from copy import deepcopy
from itertools import combinations
import heapq
from input18a import v

v=v.strip()
m = v.split('\n')
w = len(m[0])
h = len(m)
v = v.replace('\n', '')

doors = {}
keys = {}
start = None
for y, r in enumerate(m):
    for x, c in enumerate(r):
        if 'a' <= c <= 'z':
            keys[c] = (y,x)
        elif 'A' <= c <= 'Z': 
            doors[c] = (y,x)
        elif c == '@':
            start = (y,x)

def at(maze, y, x):
    return maze[y * w + x]

def dist_neighbors(p):
    y, x = p
    nbs = [(y, x+1), (y, x-1), (y - 1, x), (y + 1, x)]
    return [nb for nb in nbs if at(v, *nb) != '#']

def astar(start, end, adj, h, ln=lambda x,y:0):
    pq = []
    heapq.heappush(pq, (h(start, end), 0, start))
    visited = set()
    inq = {}
    while len(pq) > 0:
        est, act, n = heapq.heappop(pq)
        act = -act
        if n == end or (callable(end) and end(n)):
            return (act, n)
        visited.add(n)
        if n in inq:
            del inq[n]
        nbs = adj(n)
        for nb in nbs:
            d = act + ln(n, nb)
            e = d + h(nb, end)
            if nb not in visited and (nb not in inq or e < inq[nb]):
                heapq.heappush(pq, (e, -d, nb))
                inq[nb] = e

def get_paths(p, maze):
    dists = {}
    pq = [(p, ())]
    visited = set([p])
    dist = 0
    while len(pq) > 0:
        np = []
        while len(pq) > 0:
            pt, doors = pq.pop()
            y,x = pt
            c = at(maze, y, x)
            if c not in '#.@':
                dists[c] = (dist, doors)
            for p2 in dist_neighbors(pt):
                c2 = at(maze, *p2)
                if p2 not in visited and c2 != '#':
                    tdoors = doors + ((c2,) if 'A' <= c2 <= 'Z' else ())
                    np.append((p2, tdoors))
                    visited.add(p2)
        pq = np
        dist += 1
    return dists

paths = {}

for k, p in keys.items():
    paths[k] = get_paths(p, v)
for k, p in doors.items():
    paths[k] = get_paths(p, v)
paths['@'] = get_paths(start, v)

for p1, v1 in paths.items():
    for p2, v2 in v1.items():
        paths[p1][p2] = (v2[0], set([d.lower() for d in v2[1]]))

def reachable_neighbors(state):
    p, keys = state
    potential = paths[p]
    nbs = []
    skeys = set(keys)
    for n, dd in potential.items():
        if n == p:
            continue
        dist, doors = dd
        if len(doors - skeys) == 0:
            nkeys = keys
            if 'a' <= n <= 'z' and n not in keys:
                nkeys += (n,)
            nkeys = tuple(sorted(nkeys))
            nbs.append((n, nkeys))
    return nbs

def all_keys_found(state):
    p, ks = state
    return len(ks) == len(keys)

def heuristic(state, end):
    p, ks = state
    skeys = set(keys.keys())
    sks = set(ks)
    remaining_keys = skeys - sks
    if len(remaining_keys) >= 2:
        pairs = combinations(skeys - sks, 2)
        return max(paths[a][b][0] for a,b in pairs) + len(keys) - len(ks) - 1
    return len(keys) - len(ks)

def ln(start, end):
    return paths[start[0]][end[0]][0]

print(astar(('@', ()), all_keys_found, reachable_neighbors, h=heuristic, ln=ln))
