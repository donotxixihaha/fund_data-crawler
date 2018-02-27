# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN
"""
from CodeCollector import CodeCollector
from DataSaver import DataSaver
from HistoryDataCollector import HistoryDataCollector
from IPPool import IPPool
from multiprocessing import Pool
import os,time
import threading
import queue as Queue

class DataCollector(threading.Thread):
    def __init__(self, q1, q2):
        threading.Thread.__init__(self)
        self.q1 = q1
        self.q2 = q2
        self.lock = threading.RLock()
        
    def run(self):
        while True:
            try:
                code = self.q1.get(timeout = 0.5)
                hiscollector = HistoryDataCollector(code)
                history_data = hiscollector.get_data()
                self.lock.acquire()
                self.q2.put([code, history_data])
                self.lock.release()
            except:
                print('one of the read threads of PID%s ends'%os.getpid())
                break

class DataWriter(threading. Thread):
    def __init__(self, q2, i, type_):
        threading.Thread.__init__(self)
        self.i = i
        self.q2 = q2
        self.type = type_
        
    def run(self):
        while True:
            try:
                x = self.q2.get(timeout=10)
                code = x[0]
                data = x[1]
                saver = DataSaver(self.type, code)
                saver.save_to_csv(data)
                #saver.save_to_mysql(data)
            except:
                print('the write thread of %s:PID%s ends' %(self.type,os.getpid()))
                break

def mission(i):
    type_list = ['stock', 'mix', 'bond', 'all_index', 'ETFlink', 'QDII', 'LOF', 'FOF']
    print(type_list[i],end='')
    print('crawl process starts')
    ind = 5+2*i
    collector = CodeCollector()
    codelist = collector.get_code(ind)
    codeq = Queue.Queue()
    dataq = Queue.Queue()
    for code in codelist:
        codeq.put(code)
    dc1 = DataCollector(codeq, dataq)
    dc2 = DataCollector(codeq, dataq)
    dc3 = DataCollector(codeq, dataq)
    dw1 = DataWriter(dataq, i, type_list[i])
    dc1.start()
    dc2.start()
    dc3.start()
    dw1.start()
    dc1.join()
    dc2.join()
    dc3.join()
    dw1.join()
    print(type_list[i], end='')
    print('crawl process ends')    
if __name__ == '__main__':
    try:
        os.makedirs(r'D:/fund_data/stock')    
        os.makedirs(r'D:/fund_data/bond')    
        os.makedirs(r'D:/fund_data/all_index')    
        os.makedirs(r'D:/fund_data/mix')    
        os.makedirs(r'D:/fund_data/ETFlink')    
        os.makedirs(r'D:/fund_data/QDII')
        os.makedirs(r'D:/fund_data/LOF')
        os.makedirs(r'D:/fund_data/FOF')
    except:
        pass    
    start = time.time()
    pool = IPPool()
    pool.creat_proxy(10) #create an proxy pool of 10 proxies, which is enough
    codelist = []
    p = Pool()
    for i in range(8):
        p.apply_async(mission, args=(i,))
    p.close()
    p.join()       
    end = time.time()
    print('run_time = %d' %(end-start))
    
# serial code: single thread and single process
# 串行代码    
'''    
def collect(list_type,sname):
    name = sname
    for i in range(len(list_type)):
        hiscollector = HistoryDataCollector(list_type[i])
        history_data = hiscollector.get_data()
        saver = DataSaver(name,list_type[i])
        saver.save_to_mysql(history_data)        
        
    stock_list = collector.get_code(5) #股票型
    mix_list = collector.get_code(7) #混合型
    bond_list = collector.get_code(9) #债券型
    index_list = collector.get_code(11) #基金型
    ETFlink_list =  collector.get_code(13) #ETF联接
    QDII_list =  collector.get_code(15) #QDII型
    LOF_list =  collector.get_code(17) #LOF型
    FOF_list =  collector.get_code(19) #FOF型
    
    collect(stock_list,'stock')
    collect(mix_list,'mix')
    collect(bond_list,'bond')
    collect(index_list,'all_index')
    collect(ETFlink_list,'ETFlink')
    collect(QDII_list,'QDII')
    collect(LOF_list,'LOF')
    collect(FOF_list,'FOF')
'''   