'''
Created on 2016年11月2日

@author: yinkaiwen
'''
import DouBanHtml
import ChinaUtils

if __name__ == '__main__':
    tag = '中国'#可以通过改变tag来获取信息
    douban = DouBanHtml.DouBanHtml(tag);
    douban.getHtmlInfo();
    
    #如果将数据库下载下来，可以屏蔽上面3行代码，运行下面这两行代码来生成Excel表格
#     c = ChinaUtils.ChinaUtils();
#     c.saveNiceInfo();
    

