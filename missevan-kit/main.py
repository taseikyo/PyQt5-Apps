#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-25 12:51:53
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io/
# @Version : Python3.6

from ui_mwin import Ui_MWin
from PyQt5 import QtCore
from  PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QProgressBar
import re
import sys
import requests
import os
import threading
from contextlib import closing
import time
import random

base_headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Host':'www.missevan.com',
    'Pragma':'no-cache',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    }

headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Pragma':'no-cache',
    'Host':'192.168.73.133',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'X-Requested-With':'ShockwaveFlash/30.0.0.113',
}

listInfo = []

class MissevanKit(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MissevanKit, self).__init__(parent)
        self.setupUi(self)

        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget2.setColumnWidth(0, 350)

        self.connectSlots()
        if not os.path.exists('sound'):
            os.mkdir('sound')

    def connectSlots(self):
        """connect slots with buttons/
        short cuts/signals
        """
        # home tab
        self.download.clicked.connect(self.downloadSound)
        self.download.setShortcut("CTRL+L")

        self.search.clicked.connect(self.searchInfo)
        self.search.setShortcut("CTRL+Return")

        self.toolButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile("./sound")))

        # self.clearAll.clicked.connect(self.clearAllDownloaded)

    def searchInfo(self):
        text = self.lineEdit.text()
        if not text:
            return
        try:
            mid = re.findall(r'\d+', text)[-1]
            index = self.comboBox.currentIndex()
            if index == 0:
                self.getSoundSrc(mid)
            elif index == 1:
                self.getUserSound(mid)
            elif index == 2:
                self.getLikeList(mid)
        except:
            return

    def getSoundSrc(self, sid, single = True):
        """获取对应sid的下载链接
        single为假表示为列表，此时需要使用first来判断是否是列表第一个来清楚表格内容
        """
        url = 'http://www.missevan.com/sound/getsound?soundid=' + sid
        print(url)
        base_headers['Referer'] = 'http://www.missevan.com/sound/player?id=' + sid
        r =requests.get(url, headers = base_headers)
        data = r.json()
        print(type(sid))
        if data['state'] == 'error':
            return
        user = data['info']['user']['username']
        title = data['info']['sound']['soundstr']
        src = data['info']['sound']['soundurl']
        info = user+' - '+title
        # print(info)
        if single:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(1)
            item = QTableWidgetItem(sid)
            self.tableWidget.setItem(0, 0, item)
            item = QTableWidgetItem(info)
            self.tableWidget.setItem(0, 1, item)
            item = QTableWidgetItem(src)
            self.tableWidget.setItem(0, 2, item)
            self.statusBar.showMessage('共1个音声')
        else:
            item = (sid, info, src)
            listInfo.append(item)

    def getListSrc(self, sound):
        """获取对应所有sound的下载链接
        """
        global listInfo
        for x in sound:
            self.getSoundSrc(x, False)
            time.sleep(0.1+random.randint(100, 200)/100)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(listInfo))
        for r, x in enumerate(listInfo):
            for y in range(3):
                item = QTableWidgetItem(x[y])
                self.tableWidget.setItem(r, y, item)
        self.statusBar.showMessage('共{}个音声'.format(len(listInfo)))
        listInfo.clear()

    def getUserSound(self, uid):
        """获取用户的音声
        """
        p = 1
        sound = []
        while True:
            url = 'http://www.missevan.com/{uid}/getusersound?p={p}&page_size=30'.format(uid=uid, p=p)
            base_headers['Referer'] = 'http://www.missevan.com/{}/'.format(uid)
            r = requests.get(url, headers = base_headers)
            data = r.json()['info']['Datas']
            for x in data:
                count = x['view_count_formatted']
                # if count.find('万') > 0 or count.find('-') >= 0: # 获取播放量大于1万的
                #     print("次数:",count, x['id'], x['soundstr'])
                #     sound.append(str(x['id']))
                sound.append(str(x['id']))
            if not r.json()['info']['pagination']['hasMore']:
                break
            p += 1
        threading.Thread(target=self.getListSrc, args = (sound, )).start()

    def getLikeList(self, uid):
        """获取用户喜欢的声音列表
        传入用户 id
        """
        p = 1
        sound = []
        while True:
            url = 'http://www.missevan.com/{uid}/getuserlike?p={p}&page_size=30'.format(uid=uid, p=p)
            base_headers['Referer'] = 'http://www.missevan.com/{}/'.format(uid)
            r = requests.get(url, headers = base_headers)
            # pprint(r.json())
            data = r.json()['info']['Datas']
            for x in data:
                sound.append(str(x['id']))
            if not r.json()['info']['pagination']['hasMore']:
                break
            p += 1
        threading.Thread(target=self.getListSrc, args = (sound, )).start()

    def downloadSound(self):
        row = self.tableWidget.rowCount()
        row2 = self.tableWidget2.rowCount()
        # self.tableWidget2.clearContents()
        if not row:
            return
        self.tableWidget2.setRowCount(row+row2)
        for x in range(row):
            item = QTableWidgetItem(self.tableWidget.item(x, 1).text())
            self.tableWidget2.setItem(x+row2, 0, item)
            self.tableWidget2.setItem(x+row2, 1, QTableWidgetItem("下载中"))
            # qpb = QProgressBar()
            # qpb.setValue(0)
            # self.tableWidget2.setCellWidget(x, 1, qpb)
            threading.Thread(target=self.downloadSingle, args = (x+row2, )).start()

    def downloadSingle(self, index):
        url = 'http://192.168.73.133/static.missevan.com/MP3/' + self.tableWidget.item(index, 2).text()
        headers['Referer'] = 'http://www.missevan.com/sound/player?id='+ self.tableWidget.item(index, 0).text()
        title = self.tableWidget.item(index, 1).text()
        with closing(requests.get(url, headers = headers, timeout = 3, stream=True)) as r:  
            if r.status_code != 200:
                print(title, "获取资源失败！")
                return
            # print('headers:', r.headers)
            content_size = int(r.headers['content-length']) # 内容体总大小 
            chunk_size = int(content_size/100)
            # count = 0
            with open('sound/' + title+'.mp3', "wb") as file:  
                for data in r.iter_content(chunk_size=chunk_size):  
                    file.write(data)
                    # count += len(data)
            self.tableWidget2.setItem(index, 1, QTableWidgetItem("下载完成"))

    def clearAllDownloaded(self):
        row = self.tableWidget2.rowCount()
        if not row:
            return
        for x in range(row-1, -1, -1):
            if self.tableWidget2.item(x, 1).text() == '下载完成':
                self.tableWidget2.removeRow(x)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MissevanKit()
    w.show()
    sys.exit(app.exec_())