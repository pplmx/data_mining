#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/11/26 9:39
"""
    抓取网易云音乐
"""
import urllib.request

from bs4 import BeautifulSoup


def get_html(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
    return content


def parse_html(html):
    host = 'https://music.163.com'
    soup = BeautifulSoup(html, 'lxml')
    # 歌单图片[src]
    playlist_img = soup.select('ul#m-pl-container li div img')
    # 歌单名称和链接[title|href]
    playlist_name = soup.select('ul#m-pl-container li div a.msk')
    # 歌单播放量[text]
    playlist_views = soup.select('ul#m-pl-container li div.bottom span.nb')
    # 歌单创建者[title|href]
    playlist_creator = soup.select('ul#m-pl-container li p > span + a')
    for i in range(len(playlist_creator)):
        print('歌单封面: ', playlist_img[i]['src'])
        print('歌单名称: ', playlist_name[i]['title'])
        print('歌单链接: ', host + playlist_name[i]['href'])
        print('歌单播放量: ', playlist_views[i].text)
        print('歌单创建者: ', playlist_creator[i]['title'])
        print('创建者主页: ', host + playlist_creator[i]['href'], '\n')


spider_url = 'https://music.163.com/discover/playlist'
result = get_html(spider_url, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'music.163.com'
})
parse_html(result)

