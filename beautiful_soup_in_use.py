#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/11/25 21:55
"""
    beautiful soup in use
"""
import urllib.request

from bs4 import BeautifulSoup

url = "https://www.qiushibaike.com/imgrank/"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
})
response = urllib.request.urlopen(req)
content = response.read().decode('utf-8')

# 使用lxml解释器,对中文支持较好
soup = BeautifulSoup(content, 'lxml')
# css选择器
avatars = soup.select('div.author a img')
contents = soup.select('a div.content span')
pictures = soup.select('div.thumb a img')
for i in range(len(avatars)):
    # 可以根据标签的属性,获取对应的值
    avatar_url = str(avatars[i]['src']).replace('//', 'https://')
    print('作者: %s\n头像: %s\n段子信息: %s' % (avatars[i]['alt'], avatar_url, contents[i].text.replace('\n', '')))
    print(str(pictures[i]['src']).replace('//', 'https://')+'\n')
