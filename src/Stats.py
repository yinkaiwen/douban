'''
Created on 2016年11月7日

@author: yinkaiwen
计算平均数，中位数等统计数据
来源http://www.knowsky.com/885192.html（懒的写这些数学公式，值从网上找的,这个网站估计也是从别的地方转过来的，却没有写明出处）
'''
import sys

class Stats(object):

    def __init__(self, sequence):
        # sequence of numbers we will PRocess
        # convert all items to floats for numerical processing
        self.sequence = [float(item) for item in sequence]
 
    #和
    def sum(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence)
    
    #样本数量
    def count(self):
        return len(self.sequence)
 
    #最小值
    def min(self):
        if len(self.sequence) < 1:
            return None
        else:
            return min(self.sequence)
    #最大值
    def max(self):
        if len(self.sequence) < 1:
            return None
        else:
            return max(self.sequence)
 
    #平均数
    def avg(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence) / len(self.sequence)    
 
    #中位数
    def median(self):
        if len(self.sequence) < 1:
            return None
        else:
            self.sequence.sort()
            return self.sequence[len(self.sequence) // 2]
 
    #标准差
    def stdev(self):
        if len(self.sequence) < 1:
            return None
        else:
            avg = self.avg()
            sdsq = sum([(i - avg) ** 2 for i in self.sequence])
            stdev = (sdsq / (len(self.sequence) - 1)) ** .5
            return stdev
 
    def percentile(self, percentile):
        if len(self.sequence) < 1:
            value = None
        elif (percentile >= 100):
            sys.stderr.write('ERROR: percentile must be < 100.  you supplied: %s\n'% percentile)
            value = None
        else:
            element_idx = int(len(self.sequence) * (percentile / 100.0))
            self.sequence.sort()
            value = self.sequence[element_idx]
        return value
    
    
    
    
    