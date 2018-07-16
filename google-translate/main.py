#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-29 11:14:46
# @Author  : Lewis Tian (2471740600@qq.com | lewis.smith.tian@gmail.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QApplication
from mwin import Ui_MWin
import sys

class Dialog(QWidget):
    """对QWidget类重写，实现一些功能"""
    def __init__(self):
        super().__init__()
 
    # 检测键盘回车按键
    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # 举例
        if(event.key() == QtCore.Qt.Key_Escape):
            print('测试：ESC')
        if(event.key() == QtCore.Qt.Key_A):
            print('测试：A')
        if(event.key() == QtCore.Qt.Key_1):
            print('测试：1')
        if(event.key() == QtCore.Qt.Key_Enter):
            print('测试：Enter')
        if(event.key() == QtCore.Qt.Key_Space):
            print('测试：Space')
        if (event.key() == QtCore.Qt.Key_H) and QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            # self.box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.about, "谷歌翻译App", "用户名和密码不匹配！")
            # qyes=self.box.addButton("确定", QtWidgets.QMessageBox.YesRole)
            # # qno=self.box.addButton("取消", QtWidgets.QMessageBox.NoRole)
            # self.box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            # self.box.show()
            self.reply = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '谷歌翻译App v1.1',
                                            "1、输入翻译。快捷键 Ctrl+Enter 或点击按钮 \
                                             2、论文模式。需同时勾选实时翻译（监控剪贴板），会自动将回车和多个空格替换为一个空格，以及去掉一个特殊的符号 � \
                                             \n3、窗口置顶。即应用始终在桌面顶层。 " )
            self.reply.addButton(" 确 定 ", QtWidgets.QMessageBox.YesRole)
            self.reply.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.reply.setIconPixmap(QtGui.QPixmap(":/images/icon64"))
            try:
                with open('style.qss') as f: 
                    style = f.read() # 读取样式表
                    self.reply.setStyleSheet(style)
            except:
                print("open stylesheet error")
            self.reply.show()
            # reply = QtWidgets.QMessageBox.about(self,
            #                                 '谷歌翻译App',
            #                                 "1、输入翻译。快捷键 Ctrl+Enter 或点击按钮 \
            #                                  2、论文模式。需同时勾选实时翻译（监控剪贴板），会自动将回车和多个空格替换为一个空格，以及去掉一个特殊的符号 � \
            #                                  \n3、窗口置顶。即应用始终在桌面顶层。 "
            #                                 )
 
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print("鼠标左键点击")
        elif event.button() == QtCore.Qt.RightButton:
            print("鼠标右键点击")
        elif event.button() == QtCore.Qt.MidButton:
            print("鼠标中键点击")

    # def closeEvent(self, event):
    #     """
    #     重写closeEvent方法，实现dialog窗体关闭时执行一些代码
    #     :param event: close()触发的事件
    #     :return: None
    #     """
    #     reply = QtWidgets.QMessageBox.question(self,
    #                                            '谷歌翻译App',
    #                                            "是否要退出程序？",
    #                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #                                            QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = Dialog() # 创建基本窗口
    try:
        with open('style.qss') as f: 
            style = f.read() # 读取样式表
            base.setStyleSheet(style)
    except:
        print("open stylesheet error")
    w = Ui_MWin() # 创建用户界面类的实例
    w.setupUi(base) # 将用户界面加载到基本窗口
    # 监控剪贴板
    clipboard = QApplication.clipboard()
    clipboard.dataChanged.connect(w.onClipboradChanged)
    base.show() # 显示基本窗口，这样基于基本窗口的内容我们都可以看到了
    sys.exit(app.exec_())