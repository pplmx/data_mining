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


spider_url = 'https://music.163.com/#/discover/playlist'
result = get_html(spider_url, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'music.163.com'
})
print(result)
soup = BeautifulSoup(result, 'lxml')
# 歌单图片[src]
playlist_img = soup.select('ul#m-pl-container li div img')
# 歌单名称和链接[title|href]
playlist_name = soup.select('ul#m-pl-container li div a.msk')
# 歌单播放量[text]
playlist_views = soup.select('ul#m-pl-container li div.bottom span.nb')
# 歌单创建者[title|href]
playlist_creator = soup.select('ul#m-pl-container li p a')

