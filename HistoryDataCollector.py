# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
import numpy as np
import time
#import re

class HistoryDataCollector(object):
    def __init__(self, code_num):
        self.code_num = code_num
        self.proxylist = np.load(r'd:\proxy_list.npy').tolist() #load proxy pool 
        
    def get_url(self, url, header, param): 
        try:
            loc = random.randint(0,len(self.proxylist))
            proxy = self.proxylist[loc]
            r = requests.get(url, headers = header, params = param, proxies = proxy)
        except:
            r = HistoryDataCollector.get_url(self, url, header, param)  #recurs untill succedd
        return r

    def get_data(self):
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'Host': 'fund.eastmoney.com'
        }
        url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
        param = {'type':'lsjz', 'code':self.code_num, 'page':'1', 'per':'5000'}
        #r = requests.get(url, headers = headers, params = params)
        #pattern = re.compile(r'pages:\d+',re.M|re.I)
        #page_num = int(re.search(pattern,r.text[-100:]).group()[6:])
        #params['page'] = str(i)
        info_list = []
        try:
            r = requests.get(url, headers = header, params = param)
        except:
            r = HistoryDataCollector.get_url(self, url, header, param)
        soup = BeautifulSoup(r.text, 'lxml')
        for emt in soup.tbody.contents:
            info_list.append([y.string for y in emt.find_all('td')])
        col_list = [y.string for y in soup.find_all('th')]
        try:
            dataset = pd.DataFrame(info_list, columns = col_list)
        except:
            dataset = pd.DataFrame(info_list)
        else:
            dataset.iloc[:,1] = pd.to_numeric(dataset.iloc[:,1])
            dataset.iloc[:,2] = pd.to_numeric(dataset.iloc[:,2])
            day_fluc = -dataset.iloc[:,2].diff(1)/dataset.iloc[:,2]
            day_fluc.index = day_fluc.index-1
            dataset['日增长率'] = day_fluc.round(6)      
        return dataset

if __name__ == '__main__':
    start = time.time()
    manager = HistoryDataCollector('160213')
    history_data = manager.get_data()
    end = time.time()
    print(end - start)
                