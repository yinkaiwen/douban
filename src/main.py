'''
Created on 2016年11月2日

@author: yinkaiwen
'''
import DouBanHtml
from ExcelUtils import ExcelUtils

if __name__ == '__main__':
    douban = DouBanHtml.DouBanHtml('中国');
    douban.getHtmlInfo();

