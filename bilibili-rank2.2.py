'''
    2.1基础上 更新了 批量读取当天 csv 文件 用于做当天视频排行的动图
'''

import requests
from bs4 import BeautifulSoup
import csv
import datetime
import xlwt
from xlwt.Workbook import Workbook
import numpy as np
from matplotlib import pyplot as plt
import xlrd
from xlrd import sheet
import pandas as pd
import os

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
file_name_csv = f'课设\作品\data_save\\top100-{time_now}.csv'
file_name_xls = f'课设\作品\data_save\\top100-{time_now}.xls'

'''
    获取存放爬虫信息
'''
class Video:
    # 爬取信息
    def __init__(self, rank, title, score, visit, up, url, datetime):
        self.rank = rank
        self.title = title
        self.score = score
        self.visit = visit
        self.up = up
        self.url = url
        self.datetime = datetime

    # 使用静态方法直接返回数据，与上面的公有方法并无关系
    def title_save():
        return ['排名', '标题', '分数', '播放量', 'Up主', 'URL', '时间']

    # csv写入函数
    def savedata(self):
        return [self.rank, self.title, self.score, self.visit, self.up, self.url, self.datetime]

'''
    写 H5 函数
'''
def write(file_name, content_str):
    with open(file_name, 'a', encoding='UTF-8') as f:
        f.write(content_str)
        f.close

'''
    写入 csv 文件
'''
def writeTocsv(file_name_csv):
    with open(file_name_csv, 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)

        # 存放列表——writerow()
        writer.writerow(Video.title_save())

        # 行行写入
        for v in videos:
            writer.writerow(v.savedata())

'''
    用于添加数据
'''
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
        v = Video(rank, title, score.strip('\n'), visit.strip(
            '\n').strip(), up.strip('\n').strip(), url.strip('//'), time_now)
        # 将每次爬取的数据一个个添加到 videos 列表
        videos.append(v)

'''
    写入 xls
'''
def writeToxls(file_name_xls, videos):
    head = Video.title_save()
    work_book = xlwt.Workbook(encoding='UTF-8')
    # 创建工作簿并命名
    sheet = work_book.add_sheet(sheetname='BiliBili-TOP100-NOW')
    data_list = []
    # 先写表头
    for i in range(len(head)):
        sheet.write(0, i, head[i])
    for i in videos:
        data_list.append(i.savedata())

    for z in range(len(head)):
        for j in range(len(videos)):
            sheet.write(j+1, z, data_list[j][z])

    work_book.save(file_name_xls)

'''
    读取 xls 并用 plt 作图
'''
def read_xls_and_plt(file_name):
    visit = []
    work_book = xlrd.open_workbook(file_name)
    sheet_names = work_book.sheet_names()
    sheet_first = work_book.sheet_by_name(sheet_names[0])
    # 对TOP15进行取样分析
    for i in range(1, 16):
        # print(sheet_first.cell_value(i,3))
        # 格式化读取数字
        visit.append(float(sheet_first.cell_value(i, 3).strip('万')))
    # 对TOP15进行取样分析
    rank = np.arange(1, 16)
    plt.title("RANK&VISIT")
    plt.xlabel("RANK")
    plt.ylabel("VISIT")
    plt.bar(rank, visit, align='center')
    plt.show()

'''
    读取 xls 信息 并在同一幅图中进行数据对比
'''
def plt_compare(file_name):
    point_list = []
    point_list2 = []
    visit = []
    work_book = xlrd.open_workbook(file_name)
    sheet_names = work_book.sheet_names()
    sheet_first = work_book.sheet_by_name(sheet_names[0])
    # 对TOP15进行取样分析
    for i in range(1, 16):
        # print(sheet_first.cell_value(i,3))
        # 格式化读取数字
        visit.append(float(sheet_first.cell_value(i, 3).strip('万')))
    for i in range(1, 16):
        # print(sheet_first.cell_value(i,3))
        # 格式化读取数字并处理
        point_list.append(float(float(sheet_first.cell_value(i, 2).strip().strip(
            '综合得分'))/float(sheet_first.cell_value(i, 3).strip('万'))/100.0))
    for i in range(1, 16):
        # print(sheet_first.cell_value(i,3))
        # 格式化读取数字并处理
        point_list2.append(-float(float(sheet_first.cell_value(i, 2).strip().strip(
            '综合得分'))/float(sheet_first.cell_value(i, 3).strip('万'))/100.0))
    # 对TOP15进行取样分析
    rank = np.arange(1, 16)
    plt.figure(1)
    plt.title("POINT/VISIT & RANK")
    plt.plot(rank, point_list, 'r-*')
    plt.xlabel("RANK")
    plt.ylabel("VISIT")
    plt.bar(rank, visit, align='center')
    plt.show()
    plt.figure(2)
    plt.title("POINT/VISIT & RANK")
    plt.xlabel("RANK")
    plt.ylabel("POINT/VISIT")
    plt.barh(rank, point_list2)
    plt.title("point/visit & visit")
    plt.xlabel("RANK")
    plt.ylabel("VISIT")
    plt.barh(rank, visit)
    plt.text(-200, 8, 'p/v')
    plt.text(200, 9, 'visit')
    plt.show()

'''
    批量读取一天保存的csv文件

def oneday_data_trim():
    path = '课设\作品\data_save'
    files = os.listdir(path)
    csv_list = []
    for f in files:
        if os.path.splitext(f)[1] == '.csv':
            csv_list.append(path + '\\' + f)
        else:
            pass
    df = pd.read_csv(csv_list[0], low_memory=False,encoding='gbk')
    for i in range(1, len(csv_list)):
        df_i = pd.read_csv(csv_list[i], low_memory=False,encoding='gbk')
        pieces = [df[:], df_i[:]]
        df = pd.concat(pieces).drop_duplicates()
    df = df.iloc[:, [ 1, 2, 4, 6]]  # 想保留的列的编号。0为起点
    df.to_csv(path + '\\bilibiliTop_Total.csv', index=None, encoding='gbk')
'''

# 爬取数据
write('课设\作品\\bilibiliTOP100.html', r.text)
write('课设\作品\\bilibiliTOP100.txt', r.text)
appendData(videos)
writeTocsv(file_name_csv)
writeToxls(file_name_xls, videos)
# 对当前创建的xls文件直接进行数据分析
read_xls_and_plt(file_name_xls)
# 排名比较————分数与观看量的关系
plt_compare(file_name_xls)

'''
批量读取当天 csv
oneday_data_trim()
'''