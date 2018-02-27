# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN

Do not run this script very often, or your ip may be banned to arrive the website for hours
"""
import requests
from bs4 import BeautifulSoup
import chardet
import re
import numpy as np

class IPPool(object):
    def __init__(self):
        self.url = r'http://www.xicidaili.com/nn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
            }
        self.encode = chardet.detect(requests.get(self.url, headers = self.headers).content)['encoding']
        self.s = requests.Session()
        
#test whether the proxy works       
    def IPTest(self,proxy):
        link = r'http://ip.chinaz.com/getip.aspx'
        try:
            res = requests.get(link, proxies = proxy,timeout = 0.2)
            if res.status_code == 200 and res.elapsed.microseconds/1000000 <= 0.1: # 响应正常，响应时间小于0.1s，合格的代理
                return True
            else:
                return False
        except:
            return False
        
#The ip which has top 5% speed and will be alive for day level will be put into proxy pool. 
#The numberof proxies in the pool should be no less than num      
    def creat_proxy(self, num):
        self.proxies_list = []
        i = 0
        while True:
            i = i + 1
            link = self.url + str(i)
            r = self.s.get(link, headers = self.headers)
            soup = BeautifulSoup(r.text,'lxml', from_encoding = self.encode)
            for prox in soup.find_all('td', text = re.compile(r'\d+天')):
                par = prox.parent
                temp = re.findall('width:\d+%',str(par.select('div[title]')))
                try:
                    if int(temp[0][-3:-1])>=95 and int(temp[1][-3:-1])>=95:
                       ip = par.select('td')[1].string
                       port = par.select('td')[2].string
                       hp = par.select('td')[5].string.lower()
                       ipaddress = hp + r'://' + ip + ':' + port
                       proxy = { hp:ipaddress }
                       if IPPool.IPTest(self, proxy):
                           self.proxies_list.append(proxy)
                       else:
                           pass
                    else:
                        pass
                except:
                    break
            if len(self.proxies_list) >= num:
                break
        d = np.array(self.proxies_list)
        np.save(r'd:\proxy_list.npy',d) #save proxy pool as .npy file in disk D
        return self.proxies_list
        
if __name__ == '__main__':
    pool = IPPool()
    prolist = pool.creat_proxy(20)
    print(prolist)
            
