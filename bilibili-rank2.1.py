'''
    在写入数据中 更新了 时间戳，用于绘制动图做准备
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
file_name_csv = f'data_save\\top100-{time_now}.csv'
file_name_xls = f'data_save\\top100-{time_now}.xls'


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

    # 使用静态方法直接返回数据 用作写入数据的标题，与上面的公有方法并无关系
    def title_save():
        return ['排名', '标题', '分数', '播放量', 'Up主', 'URL', '时间']

    # 返回数据函数 用于之后的 csv 写入函数
    def savedata(self):
        return [self.rank, self.title, self.score, self.visit, self.up, self.url, self.datetime]


# 写入 csv

def writeTocsv(file_name_csv):
    # 打开文件 ‘w’ 写入
    with open(file_name_csv, 'w', newline='') as f:
        writer = csv.writer(f)

        # 存放列表——writerow()
        writer.writerow(Video.title_save())

        # 按行写入
        for v in videos:
            writer.writerow(v.savedata())


# 将爬取的信息存入列表

def appendData(videos):
    # 1、找到所有属于 rank-item 类的 li（列表）
    items = soup.findAll('li', {'class': 'rank-item'})

    # 2、在所有的 li 中用 Beautifulsoup 的 find 方法进行关键字遍历查找
    for itm in items:

        title = itm.find('a', {'class': 'title'}).text              # 标题
        score = itm.find('div', {'class': 'pts'}).text              # 综合得分
        rank = itm.find('div', {'class': 'num'}).text               # 排名
        visit = itm.find('span', {'class': 'data-box'}).text        # 播放量
        up = itm.find_all('a',)[2].text                             # up
        url = itm.find('a', {'class': 'title'}).get('href')         # 获取链接

        # 3、调用 Video 类方法来存放数据到 v
        # 格式化写入
        v = Video(rank, title, score.strip(), visit.strip(),
                  up.strip(), url.strip('//'), time_now)
        # 4、将每次爬取的数据一个个添加到 videos 列表
        videos.append(v)


# 写入 xls

def writeToxls(file_name_xls, videos):
    # 表头赋值
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

    # 按单元格遍历写入单元格
    for z in range(len(head)):
        for j in range(len(videos)):

            # j+1 跳过第一行(第一行已用于写入标题)
            sheet.write(j+1, z, data_list[j][z])

     # 保存 xls 文件
    work_book.save(file_name_xls)


# 读取xls数据并绘图

def read_xls_and_plt(file_name):
    # 用于——按排名存放各个视频的播放量
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
    # 顺位排名与观看量的关系
    plt.title("RANK&VISIT")
    plt.xlabel("RANK")
    plt.ylabel("VISIT")
    # 画柱状图
    plt.bar(rank, visit, align='center')
    plt.show()


# 读取xls数据画数据对比图

def plt_compare(file_name):
    # 创建 point_list 用于柱状图显示综合得分
    point_list = []
    # 创建 point_list2 用于横向柱状图进行左右数据对比
    point_list2 = []
    # 观看量
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
    # 图1
    plt.figure(1)
    # 顺位排名下 得分与观看量的比值
    plt.title("POINT/VISIT & RANK")
    # 使用红色实线 并 在取样点做⭐标记
    plt.plot(rank, point_list, 'r-*')
    plt.xlabel("RANK")
    plt.ylabel("VISIT")
    # 覆盖绘制柱状图
    plt.bar(rank, visit, align='center')
    plt.show()
    # 图2
    plt.figure(2)
    # 顺位排名下 得分与观看量的比值
    plt.title("POINT/VISIT & RANK")
    plt.xlabel("RANK")
    plt.ylabel("POINT/VISIT")
    # 绘制左横向柱状图
    plt.barh(rank, point_list2)
    plt.title("point/visit & visit")
    plt.xlabel("RANK")
    plt.ylabel("VISIT")
    # 绘制右横向柱状图
    plt.barh(rank, visit)
    # 在图上进行标识
    plt.text(-200, 8, 'p/v')
    plt.text(200, 9, 'visit')
    plt.show()


# 爬取数据
appendData(videos)
writeTocsv(file_name_csv)
writeToxls(file_name_xls, videos)
# 对当前创建的xls文件直接进行数据分析
# read_xls_and_plt(file_name_xls)
# 排名比较————分数与观看量的关系
# plt_compare(file_name_xls)
