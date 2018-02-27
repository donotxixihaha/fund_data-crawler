# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN

This script is designed to test whether your IDE is capable of using multi-process and multi-threads.
"""
from multiprocessing import Pool
import os,time
import threading

global q
q = []
for j in range(4):
    q.append([])

class writetothread(threading.Thread):
    def __init__(self, a, i):
        threading.Thread.__init__(self)
        self.a = a
        self.i = i
    def run(self):
        x = 'PID%s thread%d write' %(os.getpid(), self.a)
        print('runwrite', end='')
        print(x)
        q[self.i].append(x)
        time.sleep(1)
        
class readfromthread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
    def run(self):
        while len(q[self.i])>=1:
            x = q[self.i][0]
            q[self.i].pop(0)
            print('runread', end='')
            print(x)
            time.sleep(2)

def test(i):
    print('thread start')
    wt1 = writetothread(1, i)
    wt2 = writetothread(2, i)
    rt1 = readfromthread(i)
    wt1.start()
    wt2.start()
    rt1.start()
    wt1.join()
    wt2.join()
    rt1.join()
 
if __name__ == "__main__":
    start = time.time()
    p = Pool(processes=4)
    for i in range(4):
        p.apply_async(test, args=(i,))
    p.close()
    p.join()    
    end = time.time()
    print('runtime = %d'%(end-start))
    
     