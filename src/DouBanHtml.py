'''
Created on 2016年11月2日
@author: yinkaiwen

用于获取html中信息
'''
from urllib import request
import random
import time
from bs4 import BeautifulSoup
import re
import urllib
import CatelogDao
import IndexDao
import ExcelUtils

class DouBanHtml(object):

    def __init__(self, tag):
        self.tag = tag;
    
    def getHtmlInfo(self):  
        page = 0;
        hds = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',  
            'Opera/9.25 (Windows NT 5.1; U; en)',  
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',  
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',  
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',  
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',  
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",  
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",  
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
        ];
        totalPage = 0; 
        d = CatelogDao.CatelogDao(self.tag);
        d.createTable();
        indexDao = IndexDao.IndexDao(self.tag);
        indexDao.createTable()
        page = indexDao.getLastPage();
        print('lastpage-->',page);
        while(1):
            url = 'https://movie.douban.com/tag/' + request.quote(self.tag) + '?start=' + str(page * 20) + '&type=T'
            req = request.Request(url);
            header = hds[random.randint(0, len(hds)-1)];
            req.add_header('User-Agent', header);
            time.sleep(random.randint(1, 2))
            print(url);
            try:
                with request.urlopen(req, timeout=2) as f:
                    data = f.read();
                    print('获取到page中的数据')
                    strData = str(data, 'utf-8');
                    soup = BeautifulSoup(strData, 'html.parser');
                    # 获取总页数
                    if totalPage == 0:
                        totalPage = soup.find('span', {'class':'thispage'}).get('data-total-page');
                        totalPage = int(totalPage)
                    listSoup = soup.find('div', {'class':'article'});
                    listItem = listSoup.findAll('table');
                    for movieInfo in listItem:
                        try:
                            # 标题
                            title = movieInfo.find('a', {'class':'nbg'}).get('title')
                            title = title.replace("\"","");
                            # 详细信息地址
                            detailUrl = movieInfo.find('a', {'class':''}).get('href');
                            # 评分和评分人数tag
                            startAndNum = movieInfo.find('div', {'class':'star clearfix'})
                        except:
                            continue;
                        try:
                            # 评分
                            start = startAndNum.find('span', {'class':'rating_nums'}).string;
                        except:
                            # 评分人数不足，没有分数
                            start = '0'
                            continue;
                        
                        try:
                            # 评分人数
                            num = startAndNum.find('span', {'class':'pl'}).string;  # (12306人评价)
                            num = re.findall(r'(\w*[0-9]+)\w*', num)[0]  # 12306
                        except:
                            # 评分人数不足，
                            num = '0';
                            continue;
                        
                        detailReq = request.Request(detailUrl);
                        header = hds[random.randint(0, len(hds)-1)];
                        detailReq.add_header('User-Agent', header);
                        sleep_count = random.randint(4, 8);
                    
                        isFinish = 0;
                        while isFinish == 0:
                            time.sleep(sleep_count / 10);
                            print(detailUrl);
                            try:
                                with request.urlopen(detailReq, timeout=2) as f:
                                    data = f.read();
                                    print('获取到详细信息')
                                    strData = str(data, 'UTF-8');
                                    soup = BeautifulSoup(strData, 'html.parser');
                                    infoitem = soup.find('div', {'id':'info'})
            
                                    # 导演
                                    try:
                                        directoritem = infoitem.find('a', {'rel':'v:directedBy'})
                                        director = directoritem.string
                                    except:
                                        print('导演出错')
                                        director = '没有数据';
                                    
                                    # 编剧
                                    try:
                                        scriptwriteritems = infoitem.find_all('a', {'rel':''})
                                        scriptwriters = [];
                                        for item in scriptwriteritems:
                                            scriptwriter = item.string;
                                            scriptwriters.insert(len(scriptwriteritems), scriptwriter);
                                    except:
                                        print('编剧出错')
                                        scriptwriters = []; 
                                        
                                    scriptwriter = '';
                                    if len(scriptwriters) == 0:
                                        scriptwriter = '';
                                    else :
                                        for s in scriptwriters:
                                            scriptwriter = scriptwriter + ',' + s;
                                        scriptwriter = scriptwriter[1:];
                                         
                                    # 主演
                                    try:
                                        actorSapn = infoitem.find('span', {'class':'actor'});
                                        actoritems = actorSapn.find_all('a', {'rel':'v:starring'});
                                        actors = [];
                                        for item in actoritems:
                                            actor = item.string;
                                            actors.insert(len(actors), actor);
                                        #处理演员格式：张国荣,邓丽君,弗里德曼
                                        actor = '';
                                        for t in actors:
                                            actor = actor + ',' + t;
                                        actor = actor[1:];
                                    except:  
                                        print('演员出错')
                                        actors = [];
                                        actor = '';
                                    
                                    # 类型
                                    try:
                                        types = [];
                                        typeitems = infoitem.find_all('span', {'property':'v:genre'});
                                        
                                        for ty in typeitems:
                                            t = ty.string;
                                            types.insert(len(types), t);
                                            
                                        ty = '';
                                        for t in types:
                                            ty = ty + ',' + t;
                                        ty = ty[1:];
                                    except:
                                        types = [];
                                        print('类型出错')
                                        ty= '';
                                        
                                    # 日期(如果有两个日期，取第一个)
                                    try:
                                        dateitem = infoitem.find('span', {'property':'v:initialReleaseDate'});
                                        date = dateitem.string;
                                        rs = re.findall(r'(\w*[0-9]+\-[0-9]+\-[0-9]+)\w*', date)
                                        if len(rs) != 0 :
                                            date = rs[0];
                                        else :
                                            rs = re.findall(r'(\w*[0-9]+)\w*', date);
                                            if len(rs) > 1 :
                                                date = rs[0];
                                    except:
                                        date = '没有数据';
                                        print('日期出错')
                                    
                                    # 片长
                                    try:
                                        longitem = infoitem.find('span', {'property':'v:runtime'});
                                        longMovie = longitem.get('content');
                                    except:
                                        print('影片时长出错')
                                        longMovie = '0';
                                        
                                    # 各个评分人数的占比
                                    try:
                                        divItem = soup.find('div', {'id':'interest_sectl'});
                #                             print(divItem);
                                        perItems = divItem.find_all('span', {'class':'rating_per'});
                #                             print(perItems)
                                        stars = [];
                                        for item in perItems:
                                            starPer = item.string;
                                            starPer = re.findall(r'(\w*[0-9]+\.[0-9]+)\w*', starPer)[0];
                                            stars.insert(len(stars), starPer);
                                            
                                    except:
                                        print('评分占比出错')
                                        
                                    rs = {d.col[0] : title,
                                          d.col[1] : start,
                                          d.col[2] : num,
                                          d.col[3] : detailUrl,
                                          d.col[4] : director,
                                          d.col[5] : ty,
                                          d.col[6] : actor,
                                          d.col[7] : date,
                                          d.col[8] : longMovie,
                                          d.col[10] : stars[0],
                                          d.col[11] : stars[1],
                                          d.col[12] : stars[2],
                                          d.col[13] : stars[3],
                                          d.col[14] : stars[4],
                                          d.col[16] : scriptwriter,
                                          };
                                    print(rs)
                                    d.saveInfo(rs);
                                    isFinish = 1;
                            except urllib.error.HTTPError as e:
                                print(detailUrl,e);
                                continue;
                            except Exception as e:
                                print(e,detailUrl);
                                continue;
                            
                    indexDao.insertOrUpdateIndex(page);
                    page += 1;
                    print('下一页-->',page)
                    if page > totalPage :
                        print('page-->', page, 'totalPage-->', totalPage)
                        break;    
                    else:
                        e = ExcelUtils.ExcelUtils(self.tag);
                        e.save();
                        print('page-->', page)
            except Exception as e:
                print('获取基本信息出错:',url);
                print(e);
                continue;
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        