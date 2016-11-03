'''
Created on 2016年11月2日

@author: yinkaiwen
'''
import DouBanHtml

if __name__ == '__main__':
    tag = '中国'
    douban = DouBanHtml.DouBanHtml(tag);
    douban.getHtmlInfo();

