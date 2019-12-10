from queue import Queue
from icc import ICC
from input05 import v

v = [int(x) for x in v.strip().split(',')]

show_diagnostics = False

iq = Queue()
iq.put(1)
oq = Queue()
vm = ICC(v, iq, oq)
vm.run()
while not oq.empty():
    x = oq.get()
    if show_diagnostics or oq.empty():
        print(x)


# part 2
iq = Queue()
iq.put(5)
oq = Queue()
vm = ICC(v, iq, oq)
vm.run()
print(oq.get())
