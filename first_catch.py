#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/11/22 20:14
"""
    第一次抓取
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
pattern = re.compile('<div.*?class="content">.*?<span>(.*?)</span>.*?</a>' + '(.*?<div.*?"stats".*?</div>)',
                     re.RegexFlag.S)
items = re.findall(pattern, content)
for item in items:
    if re.search('img', item[1]):
        # 再次匹配
        patternA = re.compile('<a.*?>.*?<img src="(.*?)".*?>', re.RegexFlag.S)
        img = patternA.findall(item[1])
        print('段子：==> ' + item[0].replace('\n', ''), '\n', '段子图片：==> ' + img[0].replace('//', 'https://') + '\n')
    else:
        print('段子：==> ' + item[0].replace('\n', ''), '\n')
