import sys
import queue
import threading
from icc import ICC
from input07 import v
from itertools import permutations

v = [int(x) for x in v.strip().split(',')]


max_signal = 0
for phase_setting in permutations(range(5)):
    last = 0

    for amp in phase_setting:
        outs = []
        ip = 0
        code = [*v]
        iq = queue.Queue()
        iq.put(amp)
        iq.put(last)
        oq = queue.Queue()
        icc = ICC(v, iq, oq)
        icc.run()
        last = oq.get()
    if last > max_signal:
        max_signal = last

print('max: ', max_signal)

def run(code, iq, oq):
    icc = ICC(v, iq, oq)
    icc.run()

max_signal = 0
for phase_setting in permutations(range(5,10)):
    last = 0
    pipes = []
    for amp in phase_setting:
        q = queue.Queue()
        q.put(amp)
        pipes.append(q)
    pipes[0].put(0)
    threads = []
    for i, amp in enumerate(phase_setting):
        threads.append(
            threading.Thread(target=run, args=(v, pipes[i], pipes[(i + 1) % 5]))
        )
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    last = pipes[0].get()
    if last > max_signal:
        max_signal = last

print('max: ', max_signal)
