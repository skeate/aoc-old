from input04 import v
from hashlib import md5

v = v.strip()

x = 1
h = ''
while h[:5] != '00000':
    h = md5(f'{v}{x}'.encode('utf-8')).hexdigest()
    x += 1

print(x)

while h[:6] != '000000':
    h = md5(f'{v}{x}'.encode('utf-8')).hexdigest()
    x += 1

print(x)
