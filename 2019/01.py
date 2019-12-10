from input01 import v

v = v.strip()

s = sum(int(s) // 3 - 2 for s in v.split('\n'))
print(s)

total = 0
for x in v.split('\n'):
    print(x)
    m = int(x) // 3 - 2
    while m > 0:
        total += m
        print(m)
        m = max(0,m // 3 - 2)
print(total)
