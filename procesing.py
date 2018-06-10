import multiprocessing
import random
import time


random.seed(1)

output = multiprocessing.Queue()

def rand(length, out):
    ran = []
    for i in range(length):
        ran.append(random.randint(0, 100))
    out.put(ran)

processes = []

for i in range(4):
    p = multiprocessing.Process(target=rand, args=(5, output))
    processes.append(p)

for p in processes:
    p.start()

for p in processes:
    p.join()

for i in range(4):
    print(output.get())

#https://sebastianraschka.com/Articles/2014_multiprocessing.html