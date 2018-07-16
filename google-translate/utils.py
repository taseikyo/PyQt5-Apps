#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-29 09:41:34
# @Author  : Lewis Tian (2471740600@qq.com | lewis.smith.tian@gmail.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

"""
将其他语言翻译成中文，并将译文返回
"""

from googletrans import Translator

def trans_To_zh_CN(origin):
    """
    将origin翻译成中文，origin可以是一个字符串，也可以是一个列表
    """
    Data = []
    T = Translator(service_urls=['translate.google.cn'])
    # ts = T.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='zh-CN')
    # print('原文', origin)
    ts = T.translate(origin, dest='zh-CN')
    # print('翻译后',ts.text)
    if isinstance(ts.text, list):
        for i in ts:
            Data.append(i.text)
    else:
        return ts.text
    return Data