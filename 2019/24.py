from input24 import v

orig_state = tuple(tuple(r) for r in v.strip().split('\n'))

def neighbors(y, x):
    nbs = [(y, x+1), (y, x-1), (y - 1, x), (y + 1, x)]
    return [nb for nb in nbs if 0 <= nb[0] <= 4 and 0 <= nb[1] <= 4]

def life(s):
    nst = []
    for y, r in enumerate(s):
        nst.append([])
        for x, c in enumerate(r):
            nst[y].append(c)
            ns = neighbors(y,x)
            nbs = [n for n in ns if s[n[0]][n[1]] == '#']
            if c == '#' and len(nbs) != 1:
                nst[y][x] = '.'
            if c == '.' and 0 < len(nbs) < 3:
                nst[y][x] = '#'
    return tuple(tuple(r) for r in nst)

state = orig_state
seen = set()
while state not in seen:
    seen.add(state)
    state = life(state)

def biodiversity(s):
    bd = 0
    for y, r in enumerate(s):
        for x, c in enumerate(r):
            if c == '#':
                bd += 2**(y * 5 + x)
    return bd

print(biodiversity(state))

def pprint(s):
    for r in s:
        print(''.join(r))

def neighbors_rec(d, y, x):
    nbs = [
        (d, y, x+1),
        (d, y, x-1),
        (d, y - 1, x),
        (d, y + 1, x),
    ]
    if y == 0:
        nbs.append((d-1, 1, 2))
    elif y == 4:
        nbs.append((d-1, 3, 2))
    if x == 0:
        nbs.append((d-1, 2, 1))
    elif x == 4:
        nbs.append((d-1, 2, 3))
    if x == 2 and y == 1:
        for m in range(5):
            nbs.append((d + 1, 0, m))
    elif x == 2 and y == 3:
        for m in range(5):
            nbs.append((d + 1, 4, m))
    elif x == 1 and y == 2:
        for m in range(5):
            nbs.append((d + 1, m, 0))
    elif x == 3 and y == 2:
        for m in range(5):
            nbs.append((d + 1, m, 4))
    return [(nd,ny,nx) for nd,ny,nx in nbs if 0<=ny<=4 and 0<=nx<=4 and (ny,nx) != (2,2)]

def life_rec(s):
    nst = []
    outermost = [
            list('.....'),
            list('.....'),
            list('.....'),
            list('.....'),
            list('.....'),
        ]
    prepend = False
    if 1 <= s[0][0].count('#') <= 2:
        prepend = True
        outermost[1][2] = '#'
    if 1 <= s[0][4].count('#') <= 2:
        prepend = True
        outermost[3][2] = '#'
    if 1 <= [s[0][k][0] for k in range(5)].count('#') <= 2:
        prepend = True
        outermost[2][1] = '#'
    if 1 <= [s[0][k][4] for k in range(5)].count('#') <= 2:
        prepend = True
        outermost[2][3] = '#'

    for d, st in enumerate(s):
        nst.append([])
        for y, r in enumerate(st):
            nst[d].append([])
            for x, c in enumerate(r):
                nst[d][y].append(c)
                if y == 2 and x == 2:
                    continue

                ns = neighbors_rec(d,y,x)
                nbs = [(nd,ny,nx) for nd,ny,nx in ns if 0<=nd<len(s) and s[nd][ny][nx] == '#']
                # print(d, y, x, '::', nbs)
                if c == '#' and len(nbs) != 1:
                    nst[d][y][x] = '.'
                if c == '.' and 0 < len(nbs) < 3:
                    nst[d][y][x] = '#'
    above = s[-1][1][2] == '#'
    left = s[-1][2][1] == '#'
    right = s[-1][2][3] == '#'
    below = s[-1][3][2] == '#'
    innermost = [
        list('#####' if above else '.....'),
        list('.....'),
        list('.....'),
        list('.....'),
        list('#####' if below else '.....'),
    ]
    append = above or left or right or below
    if left:
        for k in range(5):
            innermost[k][0] = '#'
    if right:
        for k in range(5):
            innermost[k][4] = '#'
    if prepend:
        nst.insert(0, outermost)
    if append:
        nst.append(innermost)

    return nst

def pprint_rec(s):
    for d,sd in enumerate(s):
        print()
        print('depth',d)
        pprint(sd)

def life_rec_n(os, n):
    s = os
    # pprint_rec(s)
    for t in range(n):
        s = life_rec(s)
        # pprint_rec(s)
    return s

def count_bugs(s):
    b = 0
    for d in s:
        for r in d:
            for c in r:
                if c == '#':
                    b += 1
    return b
