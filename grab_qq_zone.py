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
import time

import xlrd as xlrd
import xlwt as xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
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


if __name__ == '__main__':
    # 爬取QQ空间好友动态,并保存到本地
    # myself = input('Please input your QQ: ')
    # upwd = input('Please input your password: ')
    # friend = input('Please input your friend QQ: ')
    # save_path = 'd:/' + friend + '.csv'
    # get_shuoshuo(myself, upwd, friend, save_path)
    # 读取csv文件
    # csv模块读取csv文件
    with open('d:/ss.csv', 'rt', encoding='UTF-8') as file:
        read_csv = csv.reader(file)
        all_moods = [mood for mood in read_csv]
    # pandas模块读取csv文件
    # moods = pandas.read_csv('d:/ss.csv', encoding='UTF-8')
    # print(moods.head())
    # for i in range(len(moods)):
    #     print(moods.iloc[i, 0], '==>', moods.iloc[i, 1])
