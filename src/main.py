'''
Created on 2016年11月2日

@author: yinkaiwen
'''
from src.http.DouBanHtml import DouBanHtml

if __name__ == '__main__':
    douban = DouBanHtml('中国');
    douban.getHtmlInfo();
    pass