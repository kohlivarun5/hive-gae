from Queue import Queue
from threading import Thread

_MAX_THREADS=10

def do(f,inputs,min_threads=4):

    if len(inputs) < min_threads:
        min_threads = len(inputs)


    num_threads = min_threads
    if num_threads > _MAX_THREADS:
        num_threads = _MAX_THREADS

    q = Queue()
    o = Queue()

    for i in range(num_threads):
      worker = Thread(target=_exec_solo, args=(f,q,o))
      worker.setDaemon(True)
      worker.start()

    for input in inputs:
      q.put(input)
    
    q.join()

    results = []
    while not o.empty():
        results.append(o.get())

    return results

def _exec_solo(f,q,o):
    o.put(f(q.get()))
    q.task_done()
