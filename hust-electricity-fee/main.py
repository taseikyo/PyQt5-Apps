#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-22 22:06:57
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io/
# @Version : Python3.6
# @Description : this app is to query electricity fee from http://202.114.18.218/Main.aspx

from mwin import Ui_MWin
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QUrl
from  PyQt5.QtGui import QDesktopServices
import requests
import sys
import re
import os
from urllib.parse import quote
from bs4 import BeautifulSoup as Soup
import time

class MyWindow(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        try:
            with open('style.qss') as f: 
                style = f.read() # style sheet
                self.setStyleSheet(style)
        except:
            print("open stylesheet error")

        # values initialization
        self.ss = requests.Session()
        self.__VIEWSTATE, self.__EVENTVALIDATION = self.httpRequest()
        self.txtyq = ''
        self.__EVENTTARGET = ''
        self.roomNum = '000'

        # connect ComboBox slots
        self.areaBox.currentIndexChanged.connect(self.areaBoxChanged)
        self.buildingBox.currentIndexChanged.connect(self.buildingBoxChanged)

        # connect buttons slots
        self.queryBtn.clicked.connect(self.queryFee)
        self.queryBtn.setShortcut('Ctrl+Return')
        self.cancelBtn.clicked.connect(self.reload)

        # timer define
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start()

        # Ctrl+h for help
        self.help.setShortcut('Ctrl+H')
        self.help.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/LewisTian/PyQt5-Apps/tree/master/hust-electricity-fee')))

    def areaBoxChanged(self):
        """area ComboBox changed will trigger
        the building ComboBox items
        """
        if self.areaBox.currentIndex() == 0:
            return
        print(self.areaBox.currentText())
        self.__EVENTTARGET = 'programId'
        self.programId = self.areaBox.currentText()
        self.txtyq=''
        self.httpRequest('POST')

    def buildingBoxChanged(self):
        if self.buildingBox.currentIndex() == 0:
            return
        print(self.buildingBox.currentText())
        self.__EVENTTARGET = 'txtyq'
        self.txtyq=self.buildingBox.currentText()
        self.httpRequest('POST')

    def httpRequest(self, method='GET'):
        url = 'http://202.114.18.218/Main.aspx'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'Referer': 'http://202.114.18.218/Main.aspx',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # print(headers )
        if method == 'GET':
            if 'Content-Type' in headers:
                headers.pop('Content-Type')
                headers.pop('Content-Length')
            r = self.ss.get(url, headers = headers)
            try:
                __VIEWSTATE = re.findall(r'id="__VIEWSTATE" value="(.*?)"', r.text)[0]
            except Exception as e:
                __VIEWSTATE = ''
            try:
                __EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION" value="(.*?)"', r.text)[0]
            except Exception as e:
                __EVENTVALIDATION = ''
            return __VIEWSTATE, __EVENTVALIDATION
        elif method == 'POST':
            if self.__EVENTTARGET=='query':
                """if __EVENTARGUMENT=='query'=> queryBtn is clicked
                else other combox changed
                """
                data = "__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={0}&__EVENTVALIDATION={1}&programId={2}&txtyq={3}&Txtroom={4}&ImageButton1.x=0&ImageButton1.y=16&TextBox2=&TextBox3=".format(self.__VIEWSTATE, self.__EVENTVALIDATION, self.programId, self.txtyq, self.roomEdit.text())
            else:
                data = "__EVENTTARGET={0}&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={1}&__EVENTVALIDATION={2}&programId={3}&txtyq={4}&Txtroom=&TextBox2=&TextBox3=".format(self.__EVENTTARGET,self.__VIEWSTATE, self.__EVENTVALIDATION, self.programId, self.txtyq)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Content-Length'] = str(len(data))
            r = self.ss.post(url, headers = headers, data = quote(data, safe='&=', encoding=None, errors=None))
            if self.__EVENTTARGET == 'programId': 
                """areaCombox Changed =>update buildingCombox and update `val`
                buildingCombox Changed=> just update `val`
                `val`=>self.__VIEWSTATE, self.__EVENTVALIDATION
                """
            
                # print(r.text)
                options = re.findall(r'<option value=".*?">(.*?)</option>', r.text,re.S)
                # options = re.findall(r'<select name="txtyq".*?><option value=".*?">(.*?)</option><option selected="selected" value="-1">', r.text,re.S)
                # print(options[5:])
                self.buildingBox.clear()
                self.buildingBox.addItems(['-请选择-'])
                self.buildingBox.addItems(options[5:])
            # update __VIEWSTATE and __EVENTVALIDATION
            elif self.__EVENTTARGET=='query':
                if re.findall(r'不存在该户信息', r.text):
                    self.chargeTable.setText("不存在该户信息!")
                else:
                    try:
                        check = re.findall(r'<input name="TextBox2".*?value="(.*?)" readonly="readonly" id="TextBox2" />', r.text)[0]
                        left = re.findall(r'<input name="TextBox3".*?value="(.*?)" readonly="readonly" id="TextBox3" />', r.text)[0]
                    except:
                        check = 'None'
                        left = 'None'
                    try:
                        # checkTable = re.findall(r'(<table cellspacing="0".*?id="GridView2".*?>.*?</table>)', r.text, re.S)[0]
                        chargeTable = re.findall(r'(<table cellspacing="0".*?id="GridView2".*?>.*</table>).*?</div>.*?</td>', r.text, re.S)[0]
                        print(chargeTable)
                    except:
                        print(r.text)
                        # checkTable = 'None'
                        chargeTable = 'None'
                    print(check, left)
                    self.checkEdit.setText(check)
                    self.leftEdit.setText(left)
                    # self.checkTable.setText(checkTable)
                    self.chargeTable.setText(chargeTable)
            try:
                __VIEWSTATE = re.findall(r'id="__VIEWSTATE" value="(.*?)"', r.text)[0]
                self.__VIEWSTATE = __VIEWSTATE
            except Exception as e:
                pass
            try:
                __EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION" value="(.*?)"', r.text)[0]
                self.__EVENTVALIDATION =  __EVENTVALIDATION
            except Exception as e:
                pass
            # print(self.__VIEWSTATE, '\n',self.__EVENTVALIDATION)
        else:
            pass

    def queryFee(self):
        """query electricity fee according to 
        the information
        """
        if self.buildingBox.maxCount() < 1 or not self.roomEdit.text():
            return
        if self.roomNum == self.roomEdit.text() and self.checkEdit.text() != 'None':
            """disable frequently query 
            """
            return
        self.roomNum = self.roomEdit.text()
        print(self.roomNum)
        self.__EVENTTARGET = 'query'
        self.httpRequest('POST')

    def reload(self):
        """clear app
        """
        self.buildingBox.clear()
        self.areaBox.setCurrentIndex(0)
        self.roomEdit.clear()
        self.checkEdit.clear() 
        self.leftEdit.clear()
        self.chargeTable.clear()
        self.__VIEWSTATE, self.__EVENTVALIDATION = self.httpRequest()

    def updateTime(self):
        self.timeLabel.setText('欢迎使用，现在是{0}'.format(time.strftime("%Y/%m/%d %a %X",time.localtime())))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())