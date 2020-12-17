'''
    此版本为数据写入 xls,csv
'''
import requests
from bs4 import BeautifulSoup
import csv
import datetime
import xlwt
from xlwt.Workbook import Workbook


url = "https://www.bilibili.com/v/popular/rank/all"
h = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
     'AppleWebKit/537.36 (KHTML, like Gecko)'
     'Chrome/87.0.4280.66 Safari/537.36'
     }
r = requests.get(url, headers=h, timeout=30)
soup = BeautifulSoup(r.text, 'html.parser')
# 创建空列表用于存放爬取的数据
videos = []
# strftime 格式化输出
# time_now 获取当前时间-精确到分钟
time_now = datetime.datetime.now().strftime('%Y%m%d-%H%M')
# f 嵌入变量
file_name_csv = f'top100-{time_now}.csv'
file_name_xls = f'top100-{time_now}.xls'

class Video:
    # 爬取信息
    def __init__(self, rank, title, score, visit, up, url):
        self.rank = rank
        self.title = title
        self.score = score
        self.visit = visit
        self.up = up
        self.url = url

    # 使用静态方法直接返回数据，与上面的公有方法并无关系
    def title_save():
        return ['排名', '标题', '分数', '播放量', 'Up主', 'URL']

    # csv写入函数
    def savedata(self):
        return [self.rank, self.title, self.score, self.visit, self.up, self.url]


def writeTocsv(file_name_csv):
    with open(file_name_csv, 'w', newline='') as f:
        writer = csv.writer(f)

        # 存放列表——writerow()
        writer.writerow(Video.title_save())

        # 行行写入
        for v in videos:
            writer.writerow(v.savedata())


def appendData(videos):
    # 找到所有属于 rank-item 类的 li（列表）
    items = soup.findAll('li', {'class': 'rank-item'})
    for itm in items:
        title = itm.find('a', {'class': 'title'}).text              # 标题
        score = itm.find('div', {'class': 'pts'}).text              # 综合得分
        rank = itm.find('div', {'class': 'num'}).text               # 排名
        visit = itm.find('span', {'class': 'data-box'}).text        # 播放量
        up = itm.find_all('a',)[2].text                             # up
        url = itm.find('a', {'class': 'title'}).get('href')         # 获取链接

        # 调用 Video 类方法来存放数据到 v
        # 格式化写入
        v = Video(rank, title, score.strip('\n'), visit.strip('\n').strip(), up.strip('\n').strip(), url.strip('//'))
        # 将每次爬取的数据一个个添加到 videos 列表
        videos.append(v)


def writeToxls(file_name_xls,videos):
    head=Video.title_save()
    work_book=xlwt.Workbook(encoding='UTF-8')
    # 创建工作簿并命名
    sheet = work_book.add_sheet(sheetname='BiliBili-TOP100-NOW')
    data_list=[]
    # 先写表头
    for i in range(len(head)):
        sheet.write(0,i,head[i])
    for i in videos:
        data_list.append(i.savedata())
    
    for z in range(len(head)):
        for j in range(len(videos)):
            sheet.write(j+1,z,data_list[j][z])
            
    work_book.save(file_name_xls)




appendData(videos)
writeTocsv(file_name_csv)
writeToxls(file_name_xls,videos)