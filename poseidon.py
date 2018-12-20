# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 11:24 AM
# @Author  : mac
# @Email   : 
# @File    : poseidon.py
# @Software: PyCharm
from requests import request
import time
import json
import datetime
from pyecharts import Geo
from pyecharts import Bar
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import matplotlib.pyplot as plt
from scipy.misc import imread


def get_data(url):
    headrs = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    html = request(method='GET',url=url,headers=headrs)
    if html.status_code == 200:
        return html.content
    else:
        return None

def parse_data(html):
    json_data = json.loads(html,encoding='utf-8')['cmts']
    comments = []
    try:
        for item in json_data:
            comment = {
                'nickName':item['nickName'],
                'cityName':item['cityName'] if 'cityName' in item else '',
                'content':item['content'].strip().replace('\n',''),
                'score':item['score'],
                'startTime': item['startTime']
            }
            comments.append(comment)
        return comments
    except Exception as e:
        print(e)


def save():
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())).replace(' ','%20')
    end_time = '2018-12-07 00:00:00'
    while start_time > end_time:
        url = "http://m.maoyan.com/mmdb/comments/movie/249342.json?v=yes&offset=15&startTime="+start_time
        html = None
        try:
            html = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)
        comments = parse_data(html)
        start_time = comments[14]['startTime']
        print(start_time)
        t = datetime.datetime.now()
        start_time = time.strptime(start_time,'%Y-%m-%d %H:%M:%S')
        start_time = datetime.datetime.fromtimestamp(time.mktime(start_time))+datetime.timedelta(seconds=-1)
        start_time = time.mktime(start_time.timetuple())
        start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time)).replace(' ', '%20')
        for item in comments:
            print(item)
            with open('/Users/mac/Desktop/H5DOC/H5learn/REPTILE/comments.txt', 'a', encoding='utf-8')as f:
                f.write(item['nickName'] + ',' + item['cityName'] + ',' + item['content'] + ',' + str(item['score']) +','+ item[
                    'startTime'] + '\n')


def load_data():
    lines = []
    data = []
    with open('haiwang.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
    for item in lines:
        cityinfo = item.split()
        print(cityinfo[0],cityinfo[1])
        data.append((cityinfo[0],cityinfo[1]))

    geo = Geo('海王全国观众分布','data from maoyan',title_color="#fff",title_pos="center",width=1200,height=600,background_color=
          "#404a59")
    attr,value = geo.cast(data)
    geo.add("",attr,value,type="heatmap",
        is_random=True, visual_range=[0, 1600],
    visual_text_color="#fff",
    symbol_size=15,
    is_visualmap=True,border_color="#111",
    geo_cities_coords=None)
    geo.render('hai_wang_guan_zhong.html')


def data_bar():
    data = []
    with open('haiwangtop20.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for item in lines:
        cityinfo = item.split()
        print(cityinfo[0], cityinfo[1])
        data.append((cityinfo[0], cityinfo[1]))

    bar = Bar("《海王》评论数前20")
    attr, value = bar.cast(data)
    bar.add("海王》评论数前20", attr, value,is_label_show=True,xaxis_interval=0)
    bar.render('top20.html')

def data_wordclound():
    comments = ''
    with open('comments.txt','r') as f:
        rows = f.readlines()
        try:
            for row in rows:
                lit = row.split(',')
                if len(lit) >= 3:
                    comment = lit[2]
                    if comment != '':
                        comments += ' '.join(jieba.cut(comment.strip()))
            # print(comments)
        except Exception as  e:
            print(e)

    hai_coloring = imread('hai.jpeg')
    # 多虑没用的停止词
    stopwords = STOPWORDS.copy()
    stopwords.add('电影')
    stopwords.add('一部')
    stopwords.add('一个')
    stopwords.add('没有')
    stopwords.add('什么')
    stopwords.add('有点')
    stopwords.add('感觉')
    stopwords.add('海王')
    stopwords.add('就是')
    stopwords.add('觉得')
    stopwords.add('DC')
    bg_image = plt.imread('hai.jpeg')
    font_path = '/System/Library/Fonts/STHeiti Light.ttc'
    wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path=font_path,
                   stopwords=stopwords, max_font_size=400, random_state=50)

    wc.generate(comments)
    images_colors = ImageColorGenerator(hai_coloring)
    plt.figure()
    plt.imshow(wc.recolor(color_func=images_colors))
    plt.axis('off')
    plt.show()

# url = "http://m.maoyan.com/mmdb/comments/movie/249342.json?v=yes&offset=15&startTime=2018-12-08%2019%3A17%3A16%E3%80%82" http://m.maoyan.com/mmdb/comments/movie/249342.json?v=yes&offset=15&startTime=2018-12-08 19:16:41


if __name__ == "__main__":
    url = "http://m.maoyan.com/mmdb/comments/movie/249342.json?v=yes&offset=15&startTime="
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    current_time = current_time.replace(' ','%20',-1)
    url = '''%s%s'''%(url,current_time)
    # print(url)
    # html = get_data(url=url)
    # parse_data(html)
    # save();
    # load_data()
    # data_bar()
    data_wordclound()