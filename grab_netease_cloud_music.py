#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/11/22 20:14
"""
    抓取网易云音乐歌词
"""
import re
import urllib.request

url = "http://www.qiushibaike.com"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
})
response = urllib.request.urlopen(req)
content = response.read().decode('utf-8')
# print(content)
pattern = re.compile('<div.*?class="content">\n*?<span.*?</span>\n*?</div>')
items = re.findall(pattern, content)
for item in items:
    print(item)
