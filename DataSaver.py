# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 2018

@author: WILLIAM SHEN
"""
import MySQLdb
from sqlalchemy import create_engine

class DataSaver(object):
    def __init__(self, type_, code):
        self.type = type_
        self.code = code

# replace 'localhost' in line 20 with your own host name
# replcae 'root' in line 20 with your own user name
# replace *****' in line 20 with your password  
# replace '3306' in line 23 with your db port number       
    def save_to_mysql(self, dataframe):
        con = MySQLdb.connect(host = 'localhost', user = 'root', password = '****')
        con.query('create database if not exists %s charset utf8'%self.type)
        con = MySQLdb.connect(host = 'localhost', user = 'root', password = '*****',db=self.type)
        engine = create_engine(str('mysql+mysqldb://root:*****@localhost:3306/%s?charset=utf8'%self.type))
        dataframe.to_sql(self.code, engine, schema = self.type, if_exists = 'replace')
        con.commit()
        con.close()
    
    def save_to_csv(self, dataframe):
        dataframe.to_csv('D://fund_data//'+self.type+'//'+self.code+'.csv')
        