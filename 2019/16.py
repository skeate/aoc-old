from input16 import v as inp
from itertools import repeat, cycle, chain

v = [int(i) for i in inp.strip()]

for phase in range(100):
    o = []
    for i in range(len(v)):
        s = 0
        for j in range(i+1):
            for k in range(i+j, len(v), 4*(i+1)):
                s+= v[k]
        for j in range(i+1):
            for k in range((2 + i * 3) + j, len(v), 4*(i+1)):
                s -= v[k]
        o.append(abs(s) % 10)
    v = o
print(''.join(str(x) for x in v)[:8])

v = [int(i) for i in inp.strip()] * 10000

offset = int(''.join(str(x) for x in v[0:7]))
n = v[offset:]
for phase in range(100):
    nn = []
    s = 0
    for i in range(len(n) - 1, -1, -1):
        s += n[i]
        nn.append(s %  10)
    n = nn[::-1]

print(''.join(str(x) for x in n)[:8])
