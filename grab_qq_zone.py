#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/12/12 8:33
"""
    抓取QQ空间说说
"""
import csv
import os
import re
import time
from collections import Counter

import jieba
import xlrd as xlrd
import xlwt as xlwt
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from numpy import array
from scipy.misc import imread
from selenium import webdriver
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from xlutils.copy import copy


def is_existed(path):
    if os.path.exists(path):
        os.remove(path)
    w = xlwt.Workbook()
    w.add_sheet('Sheet1')
    w.save(path)


def write_data(data1, data2, path):
    f = xlrd.open_workbook(path)
    sheet = f.sheet_by_name('Sheet1')
    src = copy(f)
    row = sheet.nrows
    src.get_sheet(0).write(row, 0, data1)
    src.get_sheet(0).write(row, 1, data2)
    src.save(path)


# 登录QQ空间
# noinspection PyBroadException
def get_shuoshuo(my_qq, my_pwd, friend_qq, path):
    is_existed(path)
    # 使用selenium
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.set_page_load_timeout(10)
        driver.get('https://user.qzone.qq.com/{}/311'.format(friend_qq))
        time.sleep(3)
    except Exception:
        print(u'网页启动异常,请重新打开')
        time.sleep(2)
        driver.quit()
    try:
        driver.find_element_by_id('login_div')
    except Exception:
        print(u'非好友无法进入空间,无权限抓取内容')
        driver.quit()
    else:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        # 输入个人QQ
        driver.find_element_by_id('u').send_keys(my_qq)
        driver.find_element_by_id('p').clear()
        # 输入个人密码
        driver.find_element_by_id('p').send_keys(my_pwd)
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    # 判断好友是否设置了权限
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
    except Exception:
        print(u'空间加载异常,请重新打开')
        time.sleep(2)
        driver.quit()
    else:
        driver.switch_to.frame('app_canvas_frame')
        next_page = 'page'
        page = 1
        try:
            while next_page:
                pages = driver.page_source
                soup = BeautifulSoup(pages, 'lxml')
                shuoshuo_send_times = soup.select(
                    'ol#msgList li.feed div.box.bgr3 > div.ft div.info a.c_tx.c_tx3.goDetail')
                shuoshuos = soup.select('ol#msgList li.feed div.bd pre.content')
                print(u'正在抓取第%d页的内容>>>>>>>>>>' % page)
                for i in range(len(shuoshuos)):
                    data = {
                        'time': shuoshuo_send_times[i]['title'],
                        'shuos': shuoshuos[i].text
                    }
                    write_data(data['time'], data['shuos'], path)
                next_page = driver.find_element_by_link_text(u'下一页')
                page = page + 1
                next_page.click()
                time.sleep(3)
                driver.implicitly_wait(3)
            driver.quit()
        except Exception:
            print(u'抓取到%d页面结束' % page)
            driver.quit()


def shuoshuo_analysis(file_path):
    # 读取csv文件
    # csv模块读取csv文件
    with open(file_path, 'rt', encoding='UTF-8') as file:
        read_csv = csv.reader(file)
        all_moods = [mood for mood in read_csv]
        all_moods = array(all_moods)
        shuoshuos = all_moods[:, 1]
        phrases = []
        # 分割(以特殊字符,如逗号,感叹号等,进行分割)+合拼成一维列表(将所有说说文字内容合并)
        for shuoshuo in shuoshuos:
            phrases += re.split(r'[^\u4E00-\u9FA5\w]+', shuoshuo)
        # 去除空串
        phrases = list(filter(lambda phrase: phrase != '', phrases))
        words = []
        for p in phrases:
            words += jieba.cut(p, HMM=True)
        print(words)
        print(len(words))
        print(set(words))
        print(len(set(words)))
        # 去除长度为1的词
        # words = list(filter(lambda word: len(word) > 1, words))
        print(Counter(words))
        back_color = imread('pokemon.jpg')  # 解析该图片
        wc = WordCloud(background_color='white',  # 背景颜色
                       max_words=1000,  # 最大词数
                       mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                       max_font_size=100,  # 显示字体的最大值
                       stopwords=STOPWORDS.add('苟利国'),  # 使用内置的屏蔽词，再添加'苟利国'
                       font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                       random_state=42,  # 为每个词返回一个PIL颜色
                       # width=1000,  # 图片的宽
                       # height=860  #图片的长
                       )
        wc.generate(' '.join(words))
        # 基于彩色图像生成相应彩色
        image_colors = ImageColorGenerator(back_color)
        # 显示图片
        plt.imshow(wc)
        # 关闭坐标轴
        plt.axis('off')
        # 绘制词云
        plt.figure()
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off')
        # 保存图片
        wc.to_file('wordcloud4.png')


if __name__ == '__main__':
    # 爬取QQ空间好友动态,并保存到本地
    # myself = input('Please input your QQ: ')
    # upwd = input('Please input your password: ')
    # friend = input('Please input your friend QQ: ')
    # save_path = 'd:/' + friend + '.csv'
    # get_shuoshuo(myself, upwd, friend, save_path)
    shuoshuo_analysis('d:/me.csv')
