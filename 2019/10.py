import heapq
from math import atan2, pi
from input10 import v

v = v.strip().split('\n')
asteroids = set([(x,y) for y in range(len(v)) for x in range(len(v[y])) if v[y][x] == '#'])

def sweep(p):
    x1, y1 = p
    angles = {}
    for a in asteroids:
        if a == mxc:
            continue
        x2, y2 = a
        angle = -(pi + atan2(x2 - x1, y2 - y1))
        if angle == 2 * pi:
            angle = 0
        if angle not in angles:
            angles[angle] = []
        heapq.heappush(angles[angle], ((x2-x1)**2+(y2-y1)**2, a))
    return angles

mx = 0
mxc = (-1,-1)
for a in asteroids:
    others = sweep(a)
    if len(others) > mx:
        mx = len(others)
        mxc = a


print(mx)

# part 2

angles = sweep(mxc)

destroyed = 0
while destroyed < 200:
    for angle in sorted(angles.keys()):
        dest = heapq.heappop(angles[angle])
        destroyed += 1
        if destroyed == 200:
            print(dest[1][0] * 100 + dest[1][1])
            break
