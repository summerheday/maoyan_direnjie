# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 14:48:55 2018

@author: iamhe
"""

from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import Geo

f = open('狄仁杰_new.txt',encoding='UTF-8')
data = pd.read_csv(f,sep=',',header=None,encoding='UTF-8',names=['date','nickname','city','rate','comment'])

print (data.head())

#分词
comment = jieba.cut(str(data["comment"]),cut_all=False)
wl_space_split= " ".join(comment)
#导入背景图
backgroud_Image = plt.imread('xuke.jpg')
stopwords = STOPWORDS.copy()
print(" STOPWORDS.copy()",help(STOPWORDS.copy()))
#可以自行加多个屏蔽词，也可直接下载停用词表格
stopwords.add("电影")
stopwords.add("一部")
stopwords.add("一个")
stopwords.add("没有")
stopwords.add("什么")
stopwords.add("有点")
stopwords.add("这部")
stopwords.add("这个")
stopwords.add("不是")
stopwords.add("真的")
stopwords.add("感觉")
stopwords.add("觉得")
stopwords.add("还是")
stopwords.add("特别")
stopwords.add("非常")
stopwords.add("可以")
stopwords.add("因为")
stopwords.add("为了")
stopwords.add("比较")
print (stopwords)
#设置词云参数
#参数分别是指定字体/背景颜色/最大的词的大小,使用给定图作为背景形状
wc =WordCloud(width=1024,height=768,background_color='white',
              mask = backgroud_Image,font_path='C:/Windows/Fonts/simkai.ttf',
              stopwords=stopwords,max_font_size=400,
              random_state=50)
#将分词后数据传入云图
wc.generate_from_text(wl_space_split)
plt.imshow(wc)
plt.axis('off')#不显示坐标轴
plt.show()
#保存结果到本地
wc.to_file(r'xuke_wordcloud.jpg')

#评分分析
rate = data['rate'].value_counts()

sns.set_style("darkgrid")
bar_plot = sns.barplot(x=rate.index,y=(rate.values/sum(rate)),palette="muted")
plt.xticks(rotation=90)
plt.show()

#观影者分布情况
city = data.groupby(['city'])
rate_group = city['rate']
city_com = city['city'].agg(['count'])
city_com.reset_index(inplace=True)
data_map = [(city_com['city'][i],city_com['count'][i]) for i in range(0,city_com.shape[0])]
geo = Geo("狄仁杰",title_color="#fff",title_pos="center",width=1200,
          height=600,background_color="#404a59")

while True: 
    try:
        attr, val = geo.cast(data_map)
        geo.add("", attr, val, visual_range=[0, 50], visual_text_color="#fff", is_geo_effect_show=False,
                is_piecewise=True, visual_split_number=6, symbol_size=15, is_visualmap=True)
        
    except ValueError as e:
        e = str(e)
        e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名称
        for i in range(0,len(data_map)):
            if e in data_map[i]:
                data_map.pop(i)
                break
    else:
        break
geo.render('狄仁杰.html')


