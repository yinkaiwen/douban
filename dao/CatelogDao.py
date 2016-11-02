'''
Created on 2016年11月2日

@author: yinkaiwen
用来查找并存储最基本的信息：
    电影名称
    评分人数
    评分
    详细信息的URL
'''
import sqlite3

class CatelogDao(object):

    def __init__(self,tag):
        self.tag = tag;
        self.col = [
           'title',  # 名称
           'star',  # 评分
           'main_num',  # 评分人数
           'detailurl',  # 详细网址
           'director',  # 导演
           'type',  # 类型
           'actor',  # 演员
           'publish_time',  # 上映时间
           'long',  # 时长
           'country',  # 制作国家(该字段废弃，没有使用)
           'fivestar', 'fourstar', 'threestar', 'twostar', 'onestar',  # 各个评分的占比
           'comment_num',  # 影评人数
           'scriptwriters' #编剧
       ];
        self.db = 'doubanspider.db'
        self.detail = '_Detail'
    
    #创建表
    def createTable(self):
        sql = 'create table if not exists %s%s (id integer primary key autoincrement,%s text,%s real,%s integer,%s text,%s text,%s text,%s text,%s text,%s integer,%s real,%s real,%s real,%s real,%s real,%s text)'%(
             self.tag,
             self.detail,
             self.col[0],
             self.col[1],
             self.col[2],
             self.col[3],
             self.col[4],
             self.col[5],
             self.col[6],
             self.col[7],
             self.col[8],
             self.col[10],
             self.col[11],
             self.col[12],
             self.col[13],
             self.col[14],
             self.col[16]
             );
        try:
            conn = sqlite3.connect(self.db);
            cursor = conn.cursor();
            cursor.execute(sql);
        finally:
            cursor.close();
            conn.commit();
            conn.close();
            
    #保存信息
    def saveInfo(self,info):
            try:
                conn = sqlite3.connect(self.db);
                cursor = conn.cursor();
                select_sql = "select * from %s%s where %s = '%s' and %s = %s" % (self.tag,self.detail, self.col[0], info[self.col[0]], self.col[1], info[self.col[1]]);
                select = cursor.execute(select_sql);
                rs = select.fetchall();
                if len(rs) == 0:
                    sql = "insert into %s%s (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) values ('%s',%s,%s,'%s',\"%s\",'%s',\"%s\",'%s',%s,%s,%s,%s,%s,%s,\"%s\")" %(
                     self.tag,
                     self.detail,
                     self.col[0],
                     self.col[1],
                     self.col[2],
                     self.col[3],
                     self.col[4],
                     self.col[5],
                     self.col[6],
                     self.col[7],
                     self.col[8],
                     self.col[10],
                     self.col[11],
                     self.col[12],
                     self.col[13],
                     self.col[14],
                     self.col[16],
                    info[self.col[0]],
    #                 star,
                    info[self.col[1]],
    #                 main_num,
                    info[self.col[2]],
                    info[self.col[3]],
                    info[self.col[4]],
                    info[self.col[5]],
                    info[self.col[6]],
                    info[self.col[7]],
                    info[self.col[8]],
                    info[self.col[10]],
                    info[self.col[11]],
                    info[self.col[12]],
                    info[self.col[13]],
                    info[self.col[14]],
                    info[self.col[16]]
                    )
                    print(sql)
                    cursor.execute(sql);
            finally:
                cursor.close();
                conn.commit();
                conn.close();
         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        