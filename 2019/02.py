import sys
from icc import ICC
from input02 import v

v = [int(x) for x in v.strip().split(',')]
code = [*v]

def rnv(n, v):
    code[1] = n
    code[2] = v
    icc = ICC(code, None, None)
    icc.run()
    return icc.code[0]


print(rnv(12, 2))


# part 2
# actually found by inspection;
# verb just adds its value
# noun is y = 331776x + 2106513
target = 19690720
x = rnv(0, 0)
y = rnv(1, 0)
n = (target - x) // (y - x)
leftover = (target - x) % (y - x)

y = rnv(0, 1)
v = leftover // (y - x)

print(n * 100 + v)
