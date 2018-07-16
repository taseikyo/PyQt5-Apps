#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-29 11:14:46
# @Author  : Lewis Tian (2471740600@qq.com | lewis.smith.tian@gmail.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from mwin import Ui_MWin
import sys

class MWin(Ui_MWin):
    def __init__(self, parent=None):
        super(MWin, self).__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = QWidget() # 创建基本窗口
    try:
        with open('style.qss') as f: 
            style = f.read() # 读取样式表
            base.setStyleSheet(style)
    except:
        print("open stylesheet error")
    w = MWin() # 创建用户界面类的实例
    w.setupUi(base) # 将用户界面加载到基本窗口
    # 监控剪贴板
    clipboard = QApplication.clipboard()
    clipboard.dataChanged.connect(w.onClipboradChanged)
    base.show() # 显示基本窗口，这样基于基本窗口的内容我们都可以看到了
    sys.exit(app.exec_())