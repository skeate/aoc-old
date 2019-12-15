import math
from input14 import v

recipes = v.strip().split('\n')

needs = {}

def part(x):
    a, r = x.strip().split(' ')
    return (int(a), r)

for r in recipes:
    i, o = r.split(' => ')
    a, r = part(o)
    needs[r] = (a, [part(a) for a in i.split(',')])


def add_wants(wants, needs, amt):
    ore_req = 0
    for need in needs:
        a, r = need
        if r == 'ORE':
            ore_req += a * amt
            continue
        if not r in wants: wants[r] = 0
        wants[r] += a * amt
    return ore_req


def find_ore_for(fuel):
    wants = { 'FUEL': fuel }
    ore_amount = 0
    while len([v for v in wants.values() if v > 0]) > 0:
        ws = wants.copy()
        for res, amt in ws.items():
            ampro, rs = needs[res]
            need = math.ceil(amt / ampro)
            amt -= need * ampro
            ore_amount += add_wants(wants, rs, need)
            wants[res] -= need * ampro
    return ore_amount

ore_for_one = find_ore_for(1)
print(ore_for_one)

low =  6216586
high = 6216618
mid = (high - low) // 2 + low
val = find_ore_for(mid)
while mid != low and mid != high:
    if val == 1e12:
        break
    if val > 1e12:
        high = mid
    elif val < 1e12:
        low = mid
    mid = (high - low) // 2 + low
    val = find_ore_for(mid)

print(mid)
