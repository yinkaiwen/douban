'''
Created on 2016年11月3日

这个类需要手动调用才会执行
@author: yinkaiwen
'''
import sqlite3
import xlwt
import math

class ChinaUtils(object):

    def __init__(self):
        self.tag = '中国';
        self.name = '中国电影（有一定影响力）.xlsx'
        self.db = 'doubanspider.db'
        self.goodPoint = 8.0;#goodPoint以上算高分电影
        self.commentNum = 10000;#commentNum条评论以上可以进入好电影或者烂片的评比环节
        self.badPoint = 5.0;#badPoint以下算低分电影
        self.effectCommentNum = 3000;# effectCommentNum条评论以上的电影可以进入“有一定影响力”的电影评比环节
    
    # 处理数据库中的数据，并保存到excel中 
    def saveNiceInfo(self):
        try:
            conn = sqlite3.connect(self.db);
            cursor = conn.cursor();
           
            f = xlwt.Workbook()  # 创建工作簿
            ChinaUtils.saveBaseInfo(self, f,cursor);
            ChinaUtils.saveStarAndLogMainNum(self, f, cursor);
            ChinaUtils.saveGoodMovie(self, f, cursor);
            ChinaUtils.saveBadMovie(self, f, cursor);
            ChinaUtils.saveGoodMoveCountAll(self,f,cursor);
            ChinaUtils.saveBadMovieCountAll(self, f, cursor);
            f.save(self.name) #保存文件
             
            f = xlwt.Workbook();
            ChinaUtils.saveYear(self, f, cursor);
            f.save('中国电影年表.xlsx')
            
        finally:
            cursor.close();
            conn.commit();
            conn.close();
            
    # 保存烂电影到excel
    def saveBadMovie(self,f,cursor):  
        ChinaUtils.savePointMovie(self,f,cursor,self.badPoint,self.commentNum,True,'烂电影');      
        pass;
    
    # 保存好电影到excel
    def saveGoodMovie(self,f,cursor): 
        ChinaUtils.savePointMovie(self,f,cursor,self.goodPoint,self.commentNum,False,'好电影');
        pass;
    
    def savePointMovie(self,f,cursor,point,commentNum,isLower,sheetName):
        sql = "select title,star,publish_time from 中国_Detail where  long > 60 and type not like '%纪录片%'  and type not like '' and type not like '%真人秀%' and type not like '%戏曲%' and type not like '%音乐%' and main_num > commentNum and star >> point";
        sql = sql.replace("point", str(point));
        sql = sql.replace("commentNum",str(commentNum));
        if isLower:
            sql = sql.replace(">>", "<");
        else :
            sql = sql.replace(">>",">");
        select = cursor.execute(sql);
        rs = select.fetchall();
        row0 = [
        u'名称',
        u'评分',
        u'上映日期',
        u'上映年份'
        ]
        sheet1 = f.add_sheet(u'%s(%s评论以上)'%(str(sheetName),str(commentNum)), cell_overwrite_ok=True)  # 创建sheet
        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        index = 1;   
        for item in rs:
            print(item);
            title = item[0];
            star = item[1];
            time = item[2];
            year = time[0:4];
            sheet1.write(index,0,title);
            sheet1.write(index,1,star);
            sheet1.write(index,2,time);
            sheet1.write(index,3,year);
            index += 1;
        pass;
    
    #好电影数量以及年份 @self.goodPoint 来设置
    def saveGoodMoveCountAll(self,f,cursor):
        ChinaUtils.saveMovieAllCount(self,f,cursor,False);
        pass;
    
    #烂电影数量以及年份 @self.badPoint 来设置
    def saveBadMovieCountAll(self,f,cursor):
        ChinaUtils.saveMovieAllCount(self,f,cursor,True);
        pass;
    
    
    # 年限以及相应的评分
    def saveMovieAllCount(self,f,cursor,isBadMovie):
        first = 1980;#包含
        last = 2016;#包含
        y = last;
        map = {};
        
        if isBadMovie :
            point = self.badPoint;
        else:
            point = self.goodPoint;
        
        while(y >= first):
            year = str(y);
            count = ChinaUtils.saveMovieCount(self, f, cursor, point,self.commentNum,isBadMovie,y);
            map[year] = count;
            y = y-1;
            
        
        
        if isBadMovie:
            n = '烂';
            row0 = [
            u'年份',
            u'数量（评分小于%s，影评人数大于%s）'%(self.badPoint,self.commentNum),
            ]
        else :
            n = '好';
            row0 = [
            u'年份',
            u'数量（评分大于%s，影评人数大于%s）'%(self.goodPoint,self.commentNum),
            ]
            
        sheet1 = f.add_sheet(u'%s影数量年份分布'%(n), cell_overwrite_ok=True)  # 创建sheet
        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        index = 1;   
        for year in map:
            count = map[year];
            sheet1.write(index,0,year);
            sheet1.write(index,1,count);
            index += 1;
        pass;

    
    #好电影数量以及年份(指定特定的年份)
    def saveMovieCount(self,f,cursor,point,commentNum,isLower,year): 
        sql = "select count(*) from 中国_Detail where  long > 60 and type not like '%纪录片%'  and type not like '' and type not like '%真人秀%' and type not like '%戏曲%' and type not like '%音乐%' and main_num > commentNum and star > point and publish_time like '%year%'";
        sql = sql.replace("point", str(point));
        sql = sql.replace("commentNum",str(commentNum));
        if isLower:
            sql = sql.replace(">>", "<");
        else :
            sql = sql.replace(">>",">");
        print(str(year));
        sql = sql.replace('year', str(year));
        select = cursor.execute(sql);
        rs = select.fetchall();
        return rs[0][0];
     
    #first-->开始年份（包含）
    #last-->结束年份（包含）       
    def saveYear(self,f, cursor):
        first = 1980;
        last = 2016;
        y = last;
        while(y >= first):
            ChinaUtils.saveYearInfo(self, f, cursor, y);
            y = y-1;
        pass;
    
    #将相关年份的评分，ln(评分人数)等信息保存到excel中     
    def saveYearInfo(self,f,cursor,year):
        sql = "select title,star,main_num,publish_time from 中国_Detail where  long > 60 and type not like '%纪录片%'  and type not like '' and type not like '%真人秀%' and type not like '%戏曲%' and type not like '%音乐%'  and publish_time like '%year%'";
        sql = sql.replace('year',str(year)); 
        print(sql);
        select = cursor.execute(sql);
        rs = select.fetchall();
        row0 = [
        u'名称',
        u'ln(评分人数%s以上)'%(str(self.effectCommentNum)),
        u'评分',
        u'上映日期'
        ]
        sheet1 = f.add_sheet(u'评分与ln(评分人数)（%s年）'%(year), cell_overwrite_ok=True)  # 创建sheet
        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        index = 1;   
        for item in rs:
            print(item);
            title = item[0];
            star = item[1];
            log_main_num = math.log(int(item[2]));
            time = item[3];
            
            sheet1.write(index,0,title);
            sheet1.write(index,1,log_main_num);
            sheet1.write(index,2,star);
            sheet1.write(index,3,time);
            index += 1;
        pass;
    
    #经有影响力的电影的评分、ln(评分人数)保存到excel中
    def saveStarAndLogMainNum(self,f,cursor):
        sql = "select title,star,main_num from 中国_Detail where  long > 60 and type not like '%纪录片%'  and type not like '' and type not like '%真人秀%' and type not like '%戏曲%' and type not like '%音乐%' and main_num > effectCommentNum";
        sql = sql.replace('effectCommentNum',str(self.effectCommentNum));
        select = cursor.execute(sql);
        rs = select.fetchall();
        row0 = [
        u'名称',
        u'ln(评分人数%s以上)'%(str(self.effectCommentNum)),
        u'评分'
        
        ]
        sheet1 = f.add_sheet(u'评分与ln(评分人数)（影评人数大于%s）'%(str(self.effectCommentNum)), cell_overwrite_ok=True)  # 创建sheet
        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        index = 1;   
        for item in rs:
            print(item);
            title = item[0];
            star = item[1];
            log_main_num = math.log(int(item[2]));
            
            sheet1.write(index,0,title);
            sheet1.write(index,2,star);
            sheet1.write(index,1,log_main_num);
            index += 1;
        pass;
    
    #储存最基本的信息
    def saveBaseInfo(self,f,cursor):
        sql = "select * from 中国_Detail where  long > 60 and type not like '%纪录片%'  and type not like '' and type not like '%真人秀%' and type not like '%戏曲%' and type not like '%音乐%' and main_num > effectCommentNum";
        sql = sql.replace("effectCommentNum", str(self.effectCommentNum));
        select = cursor.execute(sql);
        rs = select.fetchall();
        row0 = [
        u'名称',
        u'评分',
        u'评分人数',
        u'详细地址',
        u'导演',
        u'类型',
        u'演员',
        u'日期',
        u'时长',
        u'五星占比',
        u'四星占比',
        u'三星占比',
        u'两星占比',
        u'一星占比',
        u'编剧'
        ]
        sheet1 = f.add_sheet(u'影评人数大于%s人次'%(str(self.effectCommentNum)), cell_overwrite_ok=True)  # 创建sheet
        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        
        index = 1;   
        for item in rs:
            print(item);
            title = item[1];
            star = item[2];
            main_num = item[3];
            detail_url = item[4];
            director = item[5];
            ty = item[6];
            actor = item[7];
            date = item[8];
            long = item[9];
            fiveStar = item[10];
            fourStar = item[11];
            threeStar = item[12];
            twoStar = item[13];
            oneStar = item[14];
            scriptWriter = item[15];
            
            sheet1.write(index,0,title);
            sheet1.write(index,1,star);
            sheet1.write(index,2,main_num);
            sheet1.write(index,3,detail_url);
            sheet1.write(index,4,director);
            sheet1.write(index,5,ty);
            sheet1.write(index,6,actor);
            sheet1.write(index,7,date);
            sheet1.write(index,8,long);
            sheet1.write(index,9,fiveStar);
            sheet1.write(index,10,fourStar);
            sheet1.write(index,11,threeStar);
            sheet1.write(index,12,twoStar);
            sheet1.write(index,13,oneStar);
            sheet1.write(index,14,scriptWriter);
            index += 1;
            
            