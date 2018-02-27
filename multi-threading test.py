# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN

This script is designed to test whether your IDE is capable of running multi-threads and using Queue.
"""
from multiprocessing import Pool
import os,time
import threading
import queue as Queue

class read(threading.Thread):
    def __init__(self,q1,i,q2):
        threading.Thread.__init__(self)
        self.q1 = q1
        self.a = i
        self.q2 = q2
        print('thread %d starts'%i)
    def run(self):
        while True:
            try:
                x = self.q1.get(timeout=2)
                self.q2.put((os.getpid(),self.a,x))
            except:
                break

class write(threading.Thread):
    def __init__(self,i,q2):
        threading.Thread.__init__(self)
        self.a = i
        self.q2 = q2
        print('thread %d starts'%i)
    def run(self):
        while True:
            try:
                x = self.q2.get(timeout = 5)
                print(x)
            except:
                break

def main():
    q1 = Queue.Queue()
    q2 = Queue.Queue()
    for i in range(2000):
        q1.put(i)
    t1 = read(q1,1,q2)
    t2 = read(q1,2,q2)
    t3 = write(3,q2)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    
if __name__ == "__main__":
    start = time.time()
    p = Pool(processes=4)
    for i in range(4):
        p.apply_async(main, args=())
    p.close()
    p.join()    
    end = time.time()
    print('runtime = %d'%(end-start))
   