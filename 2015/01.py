from input01 import v

v = v.strip()

opens = v.count('(')
closes = v.count(')')

print(opens-closes)

floor = 0
i = 0
for c in v:
    i += 1
    if c == '(':
        floor += 1
    elif c == ')':
        floor -= 1
    if floor < 0:
        print(i)
        exit()
