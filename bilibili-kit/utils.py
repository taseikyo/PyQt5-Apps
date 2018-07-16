#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-17 20:03:01
# @Author  : Lewis Tian (2471740600@qq.com | lewis.smith.tian@gmail.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

import requests
import re
import json
from contextlib import closing
import sys
import time

base_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Host':'www.bilibili.com',
    'Upgrade-Insecure-Requests':'1',
    # 'Cookie':'fts=1510736891; sid=7qg8oi09; pgv_pvi=8538873856; rpdid=oqllxolskpdosowmkxqqw; LIVE_BUVID=c754ecfbe444ff393c68ef48c0a0a778; LIVE_BUVID__ckMd5=bb9053b319f9e2b6; _ga=GA1.2.1208853571.1524045693; UM_distinctid=1636da663115b2-058ffe192d20bb-1781c36-144000-1636da66312552; user_face=https%3A%2F%2Fi0.hdslb.com%2Fbfs%2Fface%2F124f4e53f2b13203e6c506aac6883923095d818e.jpg; buvid3=F54249DE-2FCB-4AF2-A855-E9DB21917ADA28952infoc; CNZZDATA2724999=cnzz_eid%3D1517401423-1516092026-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1528724345; CURRENT_QUALITY=80; finger=edc6ecda; DedeUserID=9272615; DedeUserID__ckMd5=9136f822c751b2c8; SESSDATA=4653d1f4%2C1532095864%2C60d67cb5; bili_jct=10014ba1985b536abe726133fee7826e; im_notify_type_9272615=0; im_seqno_9272615=532; im_local_unread_9272615=0; bp_t_offset_9272615=132291972040282007; _dfcaptcha=2977159e716ef37e3e36658071b79921',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}

def get_info(av_num):
    try:
        av_num = re.findall(r'(av\d+)', av_num)[0]
    except:
        av_num = None
    if not av_num:
        return
    url = 'https://www.bilibili.com/video/' + av_num
    base_headers['Referer'] = url
    try:
        with open('Cookie') as f: 
            Cookie = f.read() # Cookie
            base_headers['Cookie'] = Cookie
    except:
        print("open Cookie error")
    ss = requests.Session()
    r = ss.get(url, headers = base_headers, timeout = 3)
    if r.status_code == 200:
        try:
            data = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?);\(function', r.text)[0]
            bili = json.loads(data)
            aid = bili['aid']
            title = bili['videoData']['title']
            pubtime = bili['videoData']['pubdate']
            up = bili['upData']['name']
            vtype = bili['videoData']['tname']
            cover = bili['videoData']['pic']
            desc = bili['videoData']['desc']
            cid = bili['videoData']['pages'][0]['cid']
            sex = bili['upData']['sex']
            return ('av'+aid,title,time.ctime(pubtime),up,vtype,cover,desc,cid,sex)
        except:
            print("获取视频信息失败")
    return

def get_video_links(av_num):
    url = 'https://www.bilibili.com/video/' + av_num
    # print(url)
    base_headers['Referer'] = url
    # print(headers)
    ss = requests.Session()
    r = ss.get(url, headers = base_headers, timeout = 3)
    if r.status_code == 200:
        download_link = []
        try:
            data = re.findall(r'<script>window\.__playinfo__=(.*?)</script>', r.text)[0]
            bili = json.loads(data)
            # print(bili)
            try:
                download_link.append(bili['durl'][0]['url'])
            except:
                print("获取原始视频下载地址失败")
            try:
                download_link += bili['durl'][0]['backup_url']
            except:
                print("获取备用视频下载地址失败")
        except:
            print("获取视频下载地址失败")
        if download_link:
            for i in range(len(download_link)):
                download_link[i] = download_link[i].replace("http",  "https")
            # print("下载地址", download_link)
            return download_link


def download_coer_danmu(av, src):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    }
    print(av, src)
    r = requests.get(src, headers = headers)
    name = src.split('/')[-1]
    with open(name, 'wb') as f:
        f.write(r.content)
    print("下载完成")