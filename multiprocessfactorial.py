from multiprocessing import Process, cpu_count
import time
import os

class MuchCPU(Process):
    def factorial(self, n):
        num = 1
        while n >= 1:
            num = num * n
            n = n - 1
        return num
    def run(self):
        print("process pid", os.getpid()) # get process ID
        for i in range(10):
            print(self.factorial(i))
            
if __name__ == '__main__':
    print('Running...')
    procs = [MuchCPU() for f in range(cpu_count())]
    t = time.time()

    for p in procs:
        p.start()
    
    for p in procs:
        p.join()
    
    print('work took {} seconds'.format(time.time() - t))