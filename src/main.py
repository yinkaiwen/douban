'''
Created on 2016年11月2日

@author: yinkaiwen
'''
import DouBanHtml

if __name__ == '__main__':
    tag = '中国'#可以通过改变tag来获取信息
    douban = DouBanHtml.DouBanHtml(tag);
    douban.getHtmlInfo();

