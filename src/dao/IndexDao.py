'''
Created on 2016年11月2日

@author: yinkaiwen
用来记录上次爬到哪里了。
因为界面是动态地，所以这里只是粗糙的记录，并不能准确的反应实际情况：
可能有部分数据丢失。所以建议一次性将程序跑完

'''
import sqlite3

class IndexDao(object):

    def __init__(self, tag):
        self.tag = tag;
        self.table = 'page_index';
        self.db = 'doubanspider.db'
        self.col = [
            'tag',
            'page'
            ];
    
    # 创建记录表
    def createTable(self):
        sql = "create table if not exists %s (id integer primary key autoincrement,%s '%s',%s integer)" % (self.table, self.col[0], self.tag, self.col[1]);
        try:
            conn = sqlite3.connect(self.db);
            cursor = conn.cursor();
            cursor.execute(sql);
        finally:
            cursor.close();
            conn.commit();
            conn.close();
    
    # 根据情况插入或者更新数据
    def insertOrUpdateIndex(self, page):
        select_sql = "select * from %s where %s = '中国'" % (self.table, self.col[0]);
        try:
            conn = sqlite3.connect(self.db);
            cursor = conn.cursor();
            select = cursor.execute(select_sql);
            rs = select.fetchall();
            if len(rs) == 0:
                insert_sql = "insert into %s (%s,%s) values (%s,'%s')" % (self.table, self.col[1], self.col[0], page, self.tag);
                cursor.execute(insert_sql);
            else:
                update_sql = "update %s set %s = %s where %s = '%s'" % (self.table, self.col[1], page, self.col[0], self.tag);
                cursor.execute(update_sql);
        finally:
            cursor.close();
            conn.commit();
            conn.close();    
    
    #获取上次记录的page 
    def getLastPage(self):
        select_sql = "select %s from %s where %s = '%s'"%(self.col[1],self.table,self.col[0],self.tag);  
        try:
            conn = sqlite3.connect(self.db);
            cursor = conn.cursor();
            select = cursor.execute(select_sql);
            rs = select.fetchall();
            if len(rs) == 0:
                return 0;
            else:
                return rs[0][0];
        finally:
            cursor.close();
            conn.commit();
            conn.close();   
            
            
            
            
            
