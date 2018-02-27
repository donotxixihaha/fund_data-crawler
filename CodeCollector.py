# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN
"""

from bs4 import BeautifulSoup
import time
from selenium import webdriver

class CodeCollector(object):
    def __init__(self):
        """
        options=webdriver.ChromeOptions()  
        prefs = {  
             'profile.default_content_setting_values': {'images': 2}  
              }  
        options.add_experimental_option('prefs',prefs)
        """
        self.brow = webdriver.Chrome(r'D:\Anaconda\Scripts\chromedriver.exe')
        url = r'http://fund.eastmoney.com/GP_jzzzl.html#os_0;isall_0;ft_|;pt_0'
        self.brow.get(url)
    
    def get_code(self, type_num):
        type_ = self.brow.find_element_by_css_selector(r'#tabtype > li:nth-child(%d) > a > span' %type_num)
        type_.click()                                          
        try:
            all_button = self.brow.find_element_by_xpath('//*[@id="checkall"]')
            all_button.click()
            time.sleep(3)
        except:
            pass
        finally:
            soup = BeautifulSoup(self.brow.page_source, 'lxml')
            code_list = [code.string for code in soup.find_all('td', class_ = 'bzdm')]
            self.brow.quit()
        return code_list
    
if __name__ == '__main__':
    manager = CodeCollector()
    stock_list = manager.get_code(5) #股票型
    mix_list = manager.get_code(7) #混合型
    bond_list = manager.get_code(9) #债券型
    index_list = manager.get_code(11) #基金型
    ETFlink_list =  manager.get_code(13) #ETF联接
    QDII_list =  manager.get_code(15) #QDII型
    LOF_list =  manager.get_code(17) #LOF型
    FOF_list =  manager.get_code(19) #FOF型
  