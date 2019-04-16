from input01 import v

vs = [int(x) for x in v.strip().split('\n')]

print(sum(vs))

freq = 0
visited = set()
i = 0
while freq not in visited:
    visited.add(freq)
    freq += vs[i]
    i = (i + 1) % len(vs)
print(freq)
