'''
Created on 2016年11月3日

@author: yinkaiwen

用来操作Excel表格

当网络数据读取完毕并存储到本地数据库后，调用该Class中的方法
'''
import xlwt
from CatelogDao import CatelogDao

class ExcelUtils(object):

    def __init__(self, tag):
        self.name = "%s电影信息.%s" % (tag,'xlsx');
        self.tag = tag;
    
    
    # 将数据库中的信息保存到Excel中。
    def save(self):
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
        d = CatelogDao(self.tag)
        rs = d.getInfo();
        f = xlwt.Workbook()  # 创建工作簿
        sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
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
            
        f.save(self.name) #保存文件
        
