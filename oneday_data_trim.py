'''
    批量读取文件
'''

import pandas as pd
import os

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

oneday_data_trim()