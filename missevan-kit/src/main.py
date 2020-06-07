#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-25 12:51:53
# @Author  : Lewis Tian (taseikyo@gamil.com)
# @Link    : https://taseikyo.github.io/
# @Version : Python3.6

"""
搜索：
https://www.missevan.com/dramaapi/search?s=关键字&page=1

助眠分类搜索：
https://www.missevan.com/sound/getsearch?s=关键字&p=1&type=3&page_size=30&cid=71

主播音频列表：
https://www.missevan.com/主播id/getusersound?page_size=10

单个音频：
https://www.missevan.com/sound/getsound?soundid=1530133

我的关注：
https://www.missevan.com/用户id/getuserattention?type=0&page_size=1000&p=1
"""

from ui_mwin import Ui_MWin
from PyQt5 import QtCore
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QProgressBar,
)
import os
import re
import sys
import requests
import threading
from contextlib import closing
import time
import random

base_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.missevan.com",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "X-Requested-With": "ShockwaveFlash/30.0.0.113",
}

listInfo = []


class MissevanKit(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MissevanKit, self).__init__(parent)
        self.setupUi(self)

        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget2.setColumnWidth(0, 350)

        self.connectSlots()
        if not os.path.exists("sound"):
            os.mkdir("sound")

    def connectSlots(self):
        """connect slots with buttons/
        short cuts/signals
        """
        # home tab
        self.download.clicked.connect(self.downloadSound)
        self.download.setShortcut("CTRL+L")

        self.search.clicked.connect(self.searchInfo)
        self.search.setShortcut("CTRL+Return")

        self.toolButton.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile("./sound"))
        )

        # self.clearBtn.clicked.connect(self.clearAllDownloaded)

    def searchInfo(self):
        text = self.lineEdit.text()
        if not text:
            return
        try:
            mid = re.findall(r"\d+", text)[-1]
            index = self.comboBox.currentIndex()
            if index == 0:
                self.getSoundSrc(mid)
            elif index == 1:
                self.getUserSound(mid)
            elif index == 2:
                self.getLikeList(mid)
        except:
            return

    def getSoundSrc(self, sid, single=True):
        """获取对应sid的下载链接
        single为假表示为列表，此时需要使用first来判断是否是列表第一个来清楚表格内容
        """
        url = f"http://www.missevan.com/sound/getsound?soundid={sid}"
        base_headers["Referer"] = f"http://www.missevan.com/sound/player?id={sid}"
        r = requests.get(url, headers=base_headers)
        data = r.json()
        print(data)
        if not data["success"]:
            print("getSoundSrc error")
            return
        try:
            user = data["info"]["user"]["username"]
        except:
            user = "user"
        try:
            title = data["info"]["sound"]["soundstr"]
        except:
            title = "title"
        try:
            src = data["info"]["sound"]["soundurl"]
        except Exception as e:
            src = "error - 无法获取src/付费音频"
        info = f"{user} - {title}"
        print(info)
        if single:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(0, 0, QTableWidgetItem(sid))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(info))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(src))
            self.statusBar.showMessage("共1个音声")
        else:
            item = (sid, info, src)
            listInfo.append(item)

    def getListSrc(self, sound):
        """获取对应所有sound的下载链接
        """
        global listInfo
        for x in sound:
            self.getSoundSrc(x, False)
            time.sleep(0.1 + random.randint(100, 200) / 100)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(listInfo))
        for r, x in enumerate(listInfo):
            for y in range(3):
                item = QTableWidgetItem(x[y])
                self.tableWidget.setItem(r, y, item)
        self.statusBar.showMessage(f"共{len(listInfo)}个音声")
        listInfo.clear()

    def getUserSound(self, uid):
        """获取用户的音声
        """
        p = 1
        sound = []
        while True:
            url = f"http://www.missevan.com/{uid}/getusersound?p={p}&page_size=30"
            base_headers["Referer"] = f"http://www.missevan.com/{uid}/"
            r = requests.get(url, headers=base_headers)
            data = r.json()["info"]["Datas"]
            for x in data:
                count = x["view_count_formatted"]
                # if count.find('万') > 0 or count.find('-') >= 0: # 获取播放量大于1万的
                #     print("次数:",count, x['id'], x['soundstr'])
                #     sound.append(str(x['id']))
                sound.append(str(x["id"]))
            if not r.json()["info"]["pagination"]["hasMore"]:
                break
            p += 1
        if not len(sound):
            self.noSound()
            return
        threading.Thread(target=self.getListSrc, args=(sound,)).start()

    def getLikeList(self, uid):
        """获取用户喜欢的声音列表
        传入用户 id
        """
        p = 1
        sound = []
        while True:
            url = f"http://www.missevan.com/{uid}/getuserlike?p={p}&page_size=30"
            base_headers["Referer"] = f"http://www.missevan.com/{uid}/"
            r = requests.get(url, headers=base_headers)
            print(r.json())
            data = r.json()["info"]["Datas"]
            if not data:
                break
            for x in data:
                sound.append(str(x["id"]))
            if not r.json()["info"]["pagination"]["hasMore"]:
                break
            p += 1
        if not len(sound):
            self.noSound()
            return
        threading.Thread(target=self.getListSrc, args=(sound,)).start()

    def downloadSound(self):
        row = self.tableWidget.rowCount()
        row2 = self.tableWidget2.rowCount()
        if not row:
            return
        self.tableWidget2.setRowCount(row + row2)
        for x in range(row):
            self.tableWidget2.setItem(x + row2, 0, QTableWidgetItem(self.tableWidget.item(x, 1).text()))
            self.tableWidget2.setItem(x + row2, 1, QTableWidgetItem("下载中"))
            # qpb = QProgressBar()
            # qpb.setValue(0)
            # self.tableWidget2.setCellWidget(x, 1, qpb)
            threading.Thread(target=self.downloadSingle, args=(x, row2+x)).start()

    def downloadSingle(self, index, index2):
        """index: table1的行数
        index2: table2的行数
        src正常应该类似 201709/13/xxxxxx 若第一个字符为"-" 则说明获取资源失败
        """
        url = self.tableWidget.item(index, 2).text()
        print(url)
        if url[0] == "e":
            self.tableWidget2.setItem(index2, 1, QTableWidgetItem("付费音频/下载失败"))
            return

        headers[
            "Referer"
        ] = f"http://www.missevan.com/sound/player?id={self.tableWidget.item(index, 0).text()}"
        title = self.tableWidget.item(index, 1).text()
        # 替换掉 windows 不允许出现的符号
        title = re.sub(r"[/\\:*?<>|]", "", title)
        with closing(requests.get(url, headers=headers, timeout=3, stream=True)) as r:
            if r.status_code != 200:
                self.tableWidget2.setItem(index2, 1, QTableWidgetItem("获取资源失败！"))
                print(title, "获取资源失败！")
                return
            content_size = int(r.headers["content-length"])  # 内容体总大小
            chunk_size = int(content_size / 100)
            # count = 0
            with open(f"sound/{title}.mp3", "wb") as file:
                try:
                    for data in r.iter_content(chunk_size=chunk_size):
                        file.write(data)
                except Exception as e:
                    print(e)
                    self.tableWidget2.setItem(
                        index2, 1, QTableWidgetItem("下载失败")
                    )
                    return
                    # count += len(data)
            self.tableWidget2.setItem(index2, 1, QTableWidgetItem("下载完成"))

    def clearAllDownloaded(self):
        row = self.tableWidget2.rowCount()
        if not row:
            return
        for x in range(row - 1, -1, -1):
            if self.tableWidget2.item(x, 1).text() == "下载完成":
                self.tableWidget2.removeRow(x)


    def noSound(self):
        self.statusBar.showMessage("共0个音声")
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MissevanKit()
    w.show()
    sys.exit(app.exec_())
