'''
    初版，学习使用
'''
import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.bilibili.com/v/popular/rank/all"
h = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
     'AppleWebKit/537.36 (KHTML, like Gecko)'
     'Chrome/87.0.4280.66 Safari/537.36'
     }
r = requests.get(url, headers=h, timeout=30)
soup = BeautifulSoup(r.text, 'html.parser')


def save():
    class Rank:
        def __init__(self, rank, title, point, visit, up, url):
            self.rank = rank
            self.title = title
            self.point = point
            self.visit = visit
            self.up = up
            self.url = url

        def writeTocsv(self):
            return [self.rank, self.title, self.point, self.visit, self.up, self.url]

        def csv_title():
            return ['排名', '标题', '分数', '播放量', 'UP', 'URL']

    items = soup.find_all('li', {'class': 'rank-item'})
    videos = []  # 保存提取出来的video
    for itm in items:
        title = itm.find('a', {'class': 'title'}).text  # 标题
        point = itm.find('div', {'class': 'pts'}).text  # 综合得分
        rank = itm.find('div', {'class': 'num'}).text  # 排名
        visit = itm.find('span', {'class': 'data-box'}).text  # 播放量
        up = itm.find_all('a',)[2].text  # up
        url = itm.find('a', {'class': 'title'}).get('href')  # 获取链接
        v = save(rank, title, point, visit, up, url)
        videos.append(v)

    # 保存
    file_name = '课设\作品\bilibili-top100.csv'
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(save.csv_title())
        for v in videos:
            writer.writerow(v.to_csv())


print(url)
