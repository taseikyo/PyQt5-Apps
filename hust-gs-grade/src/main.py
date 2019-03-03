#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-03 14:18:52
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mwin import Ui_MWin
from bs4 import BeautifulSoup as Soup
import sys
import os
import threading
import requests

class MWin(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MWin, self).__init__(parent)
        self.setupUi(self)

        if os.path.exists('Cookis.txt'):
            with open('Cookis.txt') as f:
                self.Cookis = f.read()
        else:
            self.Cookis = ''

        self.q = Query()
        self.q.done.connect(self.show_result)
        self.q.error.connect(self.error)

    @pyqtSlot()
    def on_in_cookie_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select Cookis','','text files(*.txt);;*.*')
        if file[0]:
            try:
                with open(file[0]) as f:
                    self.Cookis = f.read()
            except:
                pass

    @pyqtSlot()
    def on_start_clicked(self):
        if not self.Cookis:
            self.error('Import Cookis first!!!')
            return
        self.q.Cookis = self.Cookis
        self.q.start()


    def show_result(self, info):
        self.result.setText(info)
    
    def error(self, msg):
        QMessageBox.information(self, '华科研究生成绩查询', msg, QMessageBox.Ok)
                
class Query(QThread):
    done = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, Cookis=None):
        super(Query, self).__init__()
        self.Cookis = Cookis

    def run(self):
        if not self.Cookis:
            self.error.emit('Import Cookis first!!!')
            return

        url1 = 'http://yjs.hust.edu.cn/ssfw/pygl/cjgl/cjcx.do'
        url2 = 'http://yjs.hust.edu.cn/ssfw/pygl/cjgl/cjcx.do'
        headers = {
            'Connection': 'keep-alive',
            'Cookie': self.Cookis,
            'Host': 'yjs.hust.edu.cn',
            'Referer': 'http://yjs.hust.edu.cn/ssfw/index.do',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

        ss = requests.Session()

        r = ss.get(url1, headers = headers)
        r = ss.get(url2, headers = headers)

        soup = Soup(r.text, 'html5lib')
        table = soup.find('div', {'class', 'div_body'})
        self.done.emit(str(table))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MWin()
    w.show()
    sys.exit(app.exec_())