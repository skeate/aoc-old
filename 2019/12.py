from input12 import v
from math import gcd
import numpy as np

moons = np.array([
    [ 12, 0, -15],
    [ -8, -5, -10],
    [ 7, -17, 1],
    [ 2, -11, -6]
], dtype='float64')

vs = np.zeros(moons.shape)

def adjust_axis(axis):
    global moons, vs
    dds = [sum(-1 if mm[axis] < m[axis] else 1 if mm[axis] > m[axis] else 0 for mm in moons) for m in moons ]
    vs[:, axis] += dds
    moons[:, axis] += vs[:, axis]


def step():
    global moons
    for i in range(3):
        adjust_axis(i)

for i in range(1000):
    step()

print(int((np.abs(moons).sum(1) * np.abs(vs).sum(1)).sum()))

moons = np.array([
    [ 12, 0, -15],
    [ -8, -5, -10],
    [ 7, -17, 1],
    [ 2, -11, -6]
], dtype='float64')
vs = np.zeros(moons.shape)

def tuplify(axis):
    global moons,vs
    return tuple(moons[:,axis]) + tuple(vs[:,axis]) 

def axis_cycle(axis):
    seen = set()
    tup = tuplify(axis)
    c = 0
    while tup not in seen:
        seen.add(tup)
        adjust_axis(axis)
        tup = tuplify(axis)
        c += 1
    return c

def lcm(xs):
    l = xs[0]
    for x in xs[1:]:
        l *= x // gcd(l, x)
    return l

xc = axis_cycle(0)
print(xc)
yc = axis_cycle(1)
print(yc)
zc = axis_cycle(2)
print(zc)

print(lcm([xc,yc,zc]))
