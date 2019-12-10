from input08 import v

v = v.strip()

zeros = 150
layer = []
for l in range(len(v) // 150):
    lz =v[l * 150:(l*150) + 150]
    z = lz.count('0')
    if z < zeros:
        zeros = z
        layer = lz

print(layer.count('1') * layer.count('2'))

pixels = []
for r in range(6):
    pixels.append([])
    for c in range(25):
        pixels[r].append([])
        pixels[r][c] = []

for l in range(len(v) // 150):
    lz = v[l * 150:(l*150) + 150]
    for i, p in enumerate(lz):
        row = i // 25
        col = i % 25
        pixels[row][col].append(p)

for row in pixels:
    for col in row:
        for d in col:
            if d == '2':
                continue
            if d == '0':
                print(' ', end='')
            if d == '1':
                print('#', end='')
            break
        else:
            print('?', end='')
    print()
