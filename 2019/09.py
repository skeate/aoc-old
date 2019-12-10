from queue import Queue
from input09 import v
from icc import ICC

v = [int(x) for x in v.strip().split(',')]

iq = Queue()
iq.put(1)
oq = Queue()
icc = ICC(v, iq, oq)
icc.run()
while not oq.empty():
    print(oq.get())

iq = Queue()
iq.put(2)
oq = Queue()
icc = ICC(v, iq, oq)
icc.run()
while not oq.empty():
    print(oq.get())
