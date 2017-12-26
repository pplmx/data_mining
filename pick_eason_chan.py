#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/12/26 14:43
"""
    采集Eason Chan
"""
import urllib.request

from bs4 import BeautifulSoup


def pick(url, headers):
    """
        采集指定url页面的html字符串
    :param url:
    :param headers:
    :return:
    """
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
    return content


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
