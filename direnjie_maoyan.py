# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 11:32:23 2018

@author: iamhe
"""

import requests
import json
import time
import random
 
#下载第一页数据
def get_one_page(url):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:  #页面正常响应
        return response.text # 返回页面源代码
    return None
 
#解析第一页数据
def parse_ono_page(html):
    data = json.loads(html)['cmts'] #评论以json形式存储,故以json形式截取
    for item in data:
        yield{ #该方法返回一个字典
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }
 
#保存数据到文本文档
def save_to_txt():
    for i in range(1, 1001):
        url='http://m.maoyan.com/mmdb/comments/movie/341516.json?_v_=yes&offset=' + str(i)
        html = get_one_page(url)
        print('正在保存第%d页.'% i)
        for item in parse_ono_page(html):
            with open('狄仁杰.txt','a',encoding='utf-8') as f:
                f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' +str(item['rate'])+','+item['comment']+'\n')
        #反扒
        time.sleep(5 + float(random.randint(1,100)) /20) 
    
# 获取的评论可能有重复，为了最终统计的真实性，需做去重处理
def delete_repeat(old,new):
    oldfile = open(old,'r',encoding='UTF-8')
    newfile = open(new,'w',encoding='UTF-8')
    content_list = oldfile.readlines() #读取的数据集
    content_alreadly_ditinct = [] #存储不重复的评论数据
    for line in content_list:
        if line not in content_alreadly_ditinct: #评论不重复
            newfile.write(line+'\n')
            content_alreadly_ditinct.append(line)
 
if __name__ =='__main__':
    save_to_txt()
    delete_repeat(r'狄仁杰.txt', r'狄仁杰_new.txt')