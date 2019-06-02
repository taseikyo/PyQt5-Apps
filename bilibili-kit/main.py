#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-05 11:14:46
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io/
# @Version : Python3.6

from ui_mwin import Ui_MWin
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from  PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QProgressBar, QMenu, QAction
import re
import sys
import requests
import time
import json
import os
import threading
from contextlib import closing

base_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Host':'www.bilibili.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}

cur_threadId = 0 # used for a new QThread id

try:
    with open('Cookie') as f: 
        Cookie = f.read() # Cookie
        base_headers['Cookie'] = Cookie
except:
    print("open Cookie error")

class BilibiliKit(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(BilibiliKit, self).__init__(parent)
        self.setupUi(self)

        self.connectSlots()

        self.ss = requests.Session()
        self.cover = None
        self.danmu = None
        self.title = None
        self.av = 0
        self.pages = 1 # 视频分p数
        self.page = 0 # 当前下载视频的索引号（从0开始）
        self.links = None
        self.slices = 1 # 视频每p的切片
        self.slice = 0 # 当前下载切片的索引号（从0开始）
        self.row2qthread = {} # 行与 qid 的映射表

    def connectSlots(self):
        """connect slots with buttons/
        short cuts/signals
        """
        # home tab
        self.search.clicked.connect(lambda: self.searchInfo(1))
        self.search.setShortcut("CTRL+Return")

        self.download.clicked.connect(self.downloadVideo)
        self.download.setShortcut("CTRL+L")

        # download tab 
        self.startAll.clicked.connect(self.startAllThreads)
        self.pauseAll.clicked.connect(self.pauseAllThreads)
        self.clearAll.clicked.connect(self.clearAllThreads)
        self.openVideoFolder.clicked.connect(self.openDownloadedVideoFolder)
        self.downloadWidget.customContextMenuRequested.connect(self.downloadWidgetContext)

    def searchInfo(self, page = 1):
        if not self.lineEdit_input.text():
            return
        url = ''
        if page == 1:
            try:
                avNum = re.findall(r'(av\d+)', self.lineEdit_input.text())[0]
            except:
                return
            url = 'https://www.bilibili.com/video/' + avNum
        else:
            url = 'https://www.bilibili.com/video/av{}?p={}'.format(self.av, page)
        if not url:
            return
        print(url)
        r = self.ss.get(url, headers = base_headers, timeout = 3)
        info = None
        if r.status_code == 200:
            try:
                data = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?);\(function', r.text)[0]
                # print(data)
                bili = json.loads(data)
                aid = bili['aid']
                title = bili['videoData']['title']
                pubtime = bili['videoData']['pubdate']
                up = bili['upData']['name']
                vtype = bili['videoData']['tname']
                cover = bili['videoData']['pic']
                desc = bili['videoData']['desc']
                sex = bili['upData']['sex']
                # get multi-videos info
                tmp = bili['videoData']['pages']
                pages = len(tmp)
                cid = [ tmp[i]['cid'] for i in range(pages)]
                info = ('av'+aid,title,time.ctime(pubtime),up,vtype,cover,'https://comment.bilibili.com/{}.xml'.format(cid[0]),desc,sex)
            except:
                print("get video info failed!")
                return
        else:
            print('error code:', r.status_code)
            return
        # print(info)
        for x in range(len(info)):
            item = QTableWidgetItem(info[x])  
            self.tableWidget.setItem(x, 0, item)
        item = QTableWidgetItem()
        icon = QIcon()
        if info[-1] == '女':
            icon.addPixmap(QPixmap(":/images/b6"), QIcon.Normal, QIcon.Off)
        elif info[-1] == '男': 
            icon.addPixmap(QPixmap(":/images/b7"), QIcon.Normal, QIcon.Off)
        else:
            icon.addPixmap(QPixmap(":/images/b8"), QIcon.Normal, QIcon.Off)
        item.setIcon(icon)
        self.tableWidget.setItem(3, 0, item)
        item = self.tableWidget.item(3, 0)
        item.setText(info[3])
        self.title = title
        self.av = aid
        self.cover = cover
        self.pages = pages
        self.danmu =  cid # https://comment.bilibili.com/43199797.xml
        self.page = page

        self.getVideoLinks(r)

    def getVideoLinks(self, r):
        # get video download links
        download_link = []
        try:
            data = re.findall(r'<script>window\.__playinfo__=(.*?)</script>', r.text)[0]
            bili = json.loads(data)
            self.slices =  len(bili['durl'])
            download_link = bili['durl']
        except:
            print("get download links failed!")
        if download_link:
            for i in range(self.slices):
                download_link[i]['url'] = download_link[i]['url'].replace("http",  "https")
        self.links = download_link

    def downloadVideo(self):
        if not self.links:
            return
        self.tabWidget.setCurrentIndex(1)
        if self.pages > 1:
            reply = QMessageBox.question(self,
                       '哔哩哔哩工具箱 v1.1 - ©Tich',
                       '发现有多个视频文件，是否全部下载？\n若否，则仅下载第一p视频(*ﾟ∀ﾟ*)',
                       QMessageBox.Yes | QMessageBox.No,
                       QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.multiDownload()
                return
        self.singleDownload()

    def singleDownload(self):
        print('single')
        row = self.downloadWidget.rowCount()
        self.downloadWidget.setRowCount(row+1)
        item = QTableWidgetItem(self.title)
        self.downloadWidget.setItem(row, 0, item)
        item = QTableWidgetItem('p{}'.format(self.page))
        self.downloadWidget.setItem(row, 1, item)
        item = QTableWidgetItem('0/{}'.format(self.slices))
        self.downloadWidget.setItem(row, 2, item)
        qpb = QProgressBar()
        qpb.setValue(0)
        self.downloadWidget.setCellWidget(row, 3, qpb)
        # print(self.links)
        t = Downloader(self.av, self.links)
        self.row2qthread[row] = t
        t.finish.connect(self.downloaded)
        t.signal.connect(self.updateItem)
        t.cur_slice.connect(self.updateItem)
        t.start()
        # print(int(t.currentThreadId()))

    def multiDownload(self):
        print('multi-videos')
        self.singleDownload()
        for x in range(2, self.pages+1):
            print(x)
            self.searchInfo(x)
            self.singleDownload()

    def downloaded(self, t, slices):
        """finish a video downloading
        """
        print('downloaded')
        for k, v in self.row2qthread.items():
            if v == t:
                if slices == -1:
                    s = '下载出错：'+ self.downloadWidget.item(k, 0).text()
                    item = QTableWidgetItem(s)
                    self.downloadWidget.setItem(k, 0, item)
                elif slices == -2:
                    s = '结束下载：'+ self.downloadWidget.item(k, 0).text()
                    item = QTableWidgetItem(s)
                    self.downloadWidget.setItem(k, 0, item)
                else:
                    item = QTableWidgetItem('{0}/{0}'.format(slices))
                    self.downloadWidget.setItem(k, 2, item)
                    QMessageBox.about(self, '哔哩哔哩工具箱 v1.1 - ©Tich', '{} 下载完成！'.format(self.downloadWidget.item(k, 0).text()))
                break
        

    def updateItem(self, t, array):
        """update downloadWidget cell
        t: qthread
        array: (val1, [val2], flag)
        val1: contains (downloaded count)/(total count)*100 / cur_slice
        val2: total slices
        op:0 => download counts
            :1 => video slices
        """
        val = array[0]
        op = array[-1]
        for k, v in self.row2qthread.items():
            if v == t:
                if op==0:
                    self.downloadWidget.cellWidget(k, 3).setValue(val)
                else:
                    item = QTableWidgetItem('{}/{}'.format(val, array[-2]))
                    self.downloadWidget.setItem(k, 2, item)
                return
    
    def startAllThreads(self):
        """start all download thread
        """
        if self.row2qthread:
            print('start all')
            for i in self.row2qthread.values():
                i.resume()

    def pauseAllThreads(self):
        """pause all download thread
        """
        if self.row2qthread:
            print('pause all')
            for i in self.row2qthread.values():
                i.pause()

    def clearAllThreads(self):
        """stop all download thread
        """
        if self.row2qthread:
            print('clear all')
            for k, v in self.row2qthread.items():
                try:
                    v.stop()
                except Exception as e:
                    pass
            self.downloadWidget.clearContents()
            self.downloadWidget.setRowCount(0)
            self.row2qthread.clear()

    def openDownloadedVideoFolder(self):
        """open download video folder
        """
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.getcwd()+'/videos'));
        except:
            pass


    def downloadWidgetContext(self, point):
        """downloadWidget right click menu
        """
        popMenu = QMenu()
        startAThread = QAction('开始', self)
        pauseAThread = QAction('暂停', self)
        clearAThread = QAction('删除', self)

        startAThread.triggered.connect(lambda: self.operateAThread(1, point))
        pauseAThread.triggered.connect(lambda: self.operateAThread(2, point))
        clearAThread.triggered.connect(lambda: self.operateAThread(3, point))

        popMenu.addAction(startAThread)
        popMenu.addAction(pauseAThread)
        popMenu.addAction(clearAThread)

        popMenu.exec_(QCursor.pos())

    def operateAThread(self, op, pos):
        cur_row = self.downloadWidget.indexAt(pos).row()
        print(cur_row) 
        if op == 1:
            print('start')
            self.row2qthread[cur_row].resume()
        elif op == 2:
            print('pause')
            self.row2qthread[cur_row].pause()
        else:
            print('clear')
            self.row2qthread[cur_row].stop()

class Downloader(QThread):
    """download class"""
    signal = pyqtSignal(QThread, list) # 下载量信号 list: value flag
    cur_slice = pyqtSignal(QThread, list) # 切片信号 list: cur_slice totla_slices flag 
    finish = pyqtSignal(QThread, int) # 下载结束信号
    def __init__(self, av, links):
        super(Downloader, self).__init__()
        self.av = av
        self.links = links
        self.id = 0
        self.__flag = threading.Event()     # pause flag
        self.__flag.set()       # True
        self.__running = threading.Event()      # stop flag
        self.__running.set()      # True
        if not os.path.exists('videos'):
            os.mkdir('videos')

    def run(self):
        """download a video 
        may contain muti-slices videos
        """
        headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Origin':'https://www.bilibili.com',
            'Pragma':'no-cache',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        }
        headers['Referer'] = 'https://www.bilibili.com/video/' + self.av
        # print(self.links)
        cur_count = 0
        total_count = len(self.links)
        print('总切片', total_count)
        for link in self.links:
            url = link['url']
            # print(url)
            filename = re.findall(r'/(\d+-\d+-\d+.flv)', url)[0]
            while self.__running.isSet(): # 如果被设置为了true就继续，false就终止了
                print("下载", filename)
                with closing(requests.get(url, headers = headers, timeout = 3, stream=True)) as r:  
                    print(r.status_code)
                    # print('headers:', r.headers)
                    content_size = int(r.headers['content-length']) # 内容体总大小  
                    # print(link['size'])
                    # print('size:', content_size)
                    chunk_size = int(content_size/100) # 单次请求最大值 
                    # print(content_size, chunk_size)
                    count = 0
                    try:
                        with open('videos/'+filename, "wb") as file:  
                            for data in r.iter_content(chunk_size=chunk_size):
                                if not self.__running.isSet():
                                    self.finish2emit(-2)
                                    return
                                self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
                                file.write(data)
                                count += len(data)
                                downloadCount = int(count/chunk_size)
                                self.signal2emit(downloadCount)
                                # print(count/chunk_size)
                    except Exception as e:
                        self.finish2emit(-1)
                        print(e)
                        return
                cur_count += 1
                print("下载完成 %d/%d"%(cur_count, total_count))
                print(downloadCount)
                if cur_count == total_count:
                    self.finish2emit(total_count)
                    return
                else:
                    self.slice2emit(cur_count, total_count)
                break

    def pause(self):
        print('pause')
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        # self.__flag.set()
        self.__running.clear()
        self.exit()

    def signal2emit(self, val):
        self.signal.emit(self, [val, 0])

    def slice2emit(self, cur_count, total_count):
        self.cur_slice.emit(self, [cur_count, total_count, 1])

    def finish2emit(self, slices):
        self.finish.emit(self, slices)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = BilibiliKit()
    w.show()
    sys.exit(app.exec_())