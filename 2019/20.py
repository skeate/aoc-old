import numpy as np
import heapq
import time
from input20 import v

v = np.array([[*r] for r in v.split('\n')[1:-1]], dtype='unicode_')
h, w = v.shape

letters = np.where(v >= 'A')

labels = {}
neighbors = {}
rlabels = {}

def adj(p):
    return (
        (
        (p[0], p[1] - 1),
        (p[0], p[1] + 1),
        ),
        (
        (p[0] - 1, p[1]),
        (p[0] + 1, p[1]),
        ),
    )

for r,c in zip(*letters):
    x = v[r,c]
    for d in adj((r,c)):
        try:
            b = v[d[0]]
            a = v[d[1]]
            if b == '.':
                label = x + a
                value = d[0]
            elif  a == '.':
                label = b + x
                value = d[1]
            else:
                continue
            rlabels[value] = label
            if label in labels:
                neighbors[value] = labels[label]
                neighbors[labels[label]] = value
            else:
                labels[label] = value
        except:
            pass


def adj_with_warps(p):
    adjs = [
        ('l', (p[0], p[1] - 1)),
        ('r', (p[0], p[1] + 1)),
        ('u', (p[0] - 1, p[1])),
        ('d', (p[0] + 1, p[1])),
    ]
    return [
        x for x in adjs if v[x[1]] == '.'
    ] + ([('w', neighbors[p])] if p in neighbors else [])

def reverse_path(p):
    return p \
        .replace('u', 'a') \
        .replace('d', 'u') \
        .replace('a', 'd') \
        .replace('l', 'a') \
        .replace('r', 'l') \
        .replace('a', 'r') \
        [::-1]


def bi_dijkstra(start, end, adj=adj_with_warps):
    visited_s = {start: (0, '')}
    visited_e = {end: (0, '')}
    to_visit_s = [(0, start, '')]
    to_visit_e = [(0, end, '')]
    mu = float('inf')

    while len(to_visit_s) > 0 and len(to_visit_e) > 0:
        # spread start
        d, n, path = heapq.heappop(to_visit_s)
        if n in visited_e:
            d2, p2 = visited_e[n]
            td = d+d2
            if td < mu:
                mu = td
                if mu <= to_visit_s[0][0] + to_visit_e[0][0]:
                    return (td, path + reverse_path(p2))
        visited_s[n] = (d, path)
        adjs = adj(n)
        for dr, a in adjs:
            if a not in visited_s:
                heapq.heappush(to_visit_s, (d + 1, a, path + dr))

        # spread end
        d, n, path = heapq.heappop(to_visit_e)
        if n in visited_s:
            d2, p2 = visited_s[n]
            td = d+d2
            if td < mu:
                mu = td
                if mu <= to_visit_s[0][0] + to_visit_e[0][0]:
                    return (td, p2 + reverse_path(path))
        visited_e[n] = (d, path)
        adjs = adj(n)
        for dr, a in adjs:
            if a not in visited_e:
                heapq.heappush(to_visit_e, (d + 1, a, path + dr))
    return -1


ans = bi_dijkstra(labels['AA'], labels['ZZ'])
print(ans[0])



# part 2

def rec_adj_with_warps(n):
    l, p = n
    adjs = [(d, (l, x)) for d,x in [
        ('l', (p[0], p[1] - 1)),
        ('r', (p[0], p[1] + 1)),
        ('u', (p[0] - 1, p[1])),
        ('d', (p[0] + 1, p[1])),
    ] if v[x] == '.']
    jumps = []
    if p in neighbors:
        y,x = p
        if x > 3 and x < w - 3 and y > 3 and y < h - 3:
            # we're in an inner warp point
            jumps = [('w', (l + 1, neighbors[p]))]
        elif l > 0:
            jumps = [('w', (l - 1, neighbors[p]))]
    return adjs + jumps

ans2 = bi_dijkstra((0,labels['AA']), (0,labels['ZZ']), adj=rec_adj_with_warps)

print(ans2[0])
