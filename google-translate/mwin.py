# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mwin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
# from utils import trans_To_zh_CN
import re
from googletrans import Translator

GTransData = ''

class Ui_MWin(QWidget):
    def __init__(self):
        super().__init__()

    def setupUi(self, MWin):
        self.win = MWin
        self.normalWin = MWin.windowFlags()
        MWin.setWindowFlags(MWin.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        MWin.setObjectName("MWin")
        MWin.setWindowModality(QtCore.Qt.ApplicationModal)
        MWin.resize(620, 415)
        MWin.setMinimumSize(QtCore.QSize(620, 415))
        MWin.setMaximumSize(QtCore.QSize(620, 415))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon64"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MWin.setWindowIcon(icon)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MWin)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setSpacing(6)
        self.mainLayout.setObjectName("mainLayout")
        self.originLabel = QtWidgets.QLabel(MWin)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.originLabel.setFont(font)
        self.originLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.originLabel.setObjectName("originLabel")
        self.mainLayout.addWidget(self.originLabel, 0, 0, 1, 1)
        self.originText = QtWidgets.QPlainTextEdit(MWin)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.originText.setFont(font)
        self.originText.setObjectName("originText")
        self.mainLayout.addWidget(self.originText, 0, 1, 1, 1)
        self.transText = QtWidgets.QPlainTextEdit(MWin)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.transText.setFont(font)
        self.transText.setObjectName("transText")
        self.mainLayout.addWidget(self.transText, 1, 1, 1, 2)
        self.transLabel = QtWidgets.QLabel(MWin)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.transLabel.setFont(font)
        self.transLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.transLabel.setObjectName("transLabel")
        self.mainLayout.addWidget(self.transLabel, 1, 0, 1, 1)
        self.Layout = QtWidgets.QVBoxLayout()
        self.Layout.setSpacing(6)
        self.Layout.setObjectName("Layout")
        self.realTimeTrans = QtWidgets.QCheckBox(MWin)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.realTimeTrans.setFont(font)
        self.realTimeTrans.setObjectName("realTimeTrans")
        # self.realTimeTrans.setChecked(True)
        self.Layout.addWidget(self.realTimeTrans)
        self.alwaysFront = QtWidgets.QCheckBox(MWin)
        self.alwaysFront.setFont(font)
        self.alwaysFront.setObjectName("alwaysFront")
        self.alwaysFront.setChecked(True)
        self.Layout.addWidget(self.alwaysFront)
        self.paperMode = QtWidgets.QCheckBox(MWin)
        self.paperMode.setFont(font)
        self.paperMode.setObjectName("paperMode")
        self.paperMode.setChecked(True)
        self.Layout.addWidget(self.paperMode)
        self.Layout_1 = QtWidgets.QHBoxLayout()
        self.Layout_1.setSpacing(6)
        self.Layout_1.setObjectName("Layout_1")
        self.logo = QtWidgets.QLabel(MWin)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/images/icon64"))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.Layout_1.addWidget(self.logo)
        self.Layout_2 = QtWidgets.QVBoxLayout()
        self.Layout_2.setSpacing(6)
        self.Layout_2.setObjectName("Layout_2")
        self.label = QtWidgets.QLabel(MWin)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Layout_2.addWidget(self.label)
        self.go = QtWidgets.QPushButton(MWin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go.sizePolicy().hasHeightForWidth())
        self.go.setSizePolicy(sizePolicy)
        self.go.setMinimumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.go.setFont(font)
        self.go.setObjectName("go")
        self.Layout_2.addWidget(self.go)
        self.Layout_2.setStretch(0, 1)
        self.Layout_2.setStretch(1, 2)
        self.Layout_1.addLayout(self.Layout_2)
        self.Layout.addLayout(self.Layout_1)
        self.mainLayout.addLayout(self.Layout, 0, 2, 1, 1)
        self.horizontalLayout.addLayout(self.mainLayout)

        self.retranslateUi(MWin)
        QtCore.QMetaObject.connectSlotsByName(MWin)
        self.connectUI()
        self.isRealTimeTrans = self.realTimeTrans.isChecked()

    def retranslateUi(self, MWin):
        _translate = QtCore.QCoreApplication.translate
        MWin.setWindowTitle(_translate("MWin", "谷歌翻译App v1.1"))
        self.originLabel.setText(_translate("MWin", "原文："))
        self.transLabel.setText(_translate("MWin", "翻译："))
        self.originText.setPlaceholderText(_translate("MWin", "Ctrl+h 获取帮助"))
        self.realTimeTrans.setText(_translate("MWin", "实时翻译"))
        self.paperMode.setText(_translate("MWin", "论文模式"))
        self.alwaysFront.setText(_translate("MWin", "窗口置顶"))
        self.label.setText(_translate("MWin", "谷歌翻译\n小程序\n©Tich"))
        self.go.setText(_translate("MWin", "翻译"))
        self.go.setShortcut(_translate("MWin", "Ctrl+Return"))

    def connectUI(self):
        # self.originLabel.clicked.connect(self.clearOriginText) # 点击原文标签就清除文本框中的
        # self.transLabel.clicked.connect(self.clearTransText)
        self.go.clicked.connect(self.transTextToZhCN) # GO按钮点击事件
        self.alwaysFront.clicked.connect(self.alwaysFrontFunc) # 是否总是最前
        self.realTimeTrans.clicked.connect(self.realTimeTransFunc) # 是否实时翻译

    def clearOriginText(self):
        self.originText.setPlainText("")

    def clearTransText(self):
        self.transText.setPlainText("")

    def transTextToZhCN(self):
        text = self.originText.toPlainText()
        if text:
            try:
                # self.transText.setPlainText(trans_To_zh_CN(text))
                self.t=GTranslator(text)
                self.t.start()
                self.transText.setPlainText("")
                self.transText.setPlaceholderText("翻译中...")
                self.t.trigger.connect(self.translated)
            except:
                self.transText.setPlainText("翻译出错！")

    def alwaysFrontFunc(self):
        """
        修改窗口状态：是否总在前面
        """
        if self.alwaysFront.isChecked():
            # print("Front", self.win.windowFlags())
            self.win.setWindowFlags(self.win.windowFlags() | QtCore.Qt.WindowStaysOnTopHint) # 窗口最前
            self.win.show()
        else:
            # print("Back", self.win.windowFlags())
            self.win.setWindowFlags(self.normalWin | QtCore.Qt.Widget) # 取消窗口最前
            self.win.show()

    def realTimeTransFunc(self):
        """
        修改是否需要实时翻译
        此模式仅在复制文本的时候有用
        对于手动输入的无效
        """
        # print(self.isRealTimeTrans)
        self.isRealTimeTrans = self.realTimeTrans.isChecked()

    def onClipboradChanged(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text and self.isRealTimeTrans:
            content = str(text)
            # print(content)
            if self.paperMode.isChecked(): # 若是论文模式，则将换行符替换为空格
                content = re.sub(r'\n|\s+', ' ', content)
                content = re.sub(r'', '', content)
            self.originText.setPlainText(content)
            try:
                # data = trans_To_zh_CN(content)
                # self.transText.setPlainText(data)
                self.t=GTranslator(content)
                self.t.start()
                self.transText.setPlainText("")
                self.transText.setPlaceholderText("翻译中...")
                self.t.trigger.connect(self.translated)
            except:
                self.transText.setPlainText("翻译出错！")

    def translated(self):
        global GTransData
        if GTransData:
            self.transText.setPlainText(GTransData)
        else:
            self.transText.setPlainText("翻译出错！")
        GTransData = ""

class GTranslator(QThread): 
    trigger = pyqtSignal()
    def __init__(self, content):
        super().__init__()
        self.content = content
  
    def run(self): 
        """
        将origin翻译成中文，origin可以是一个字符串，也可以是一个列表
        """
        Data = []
        global GTransData
        T = Translator(service_urls=['translate.google.cn'])
        # ts = T.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='zh-CN')
        # print('原文', origin)
        ts = T.translate(self.content, dest='zh-CN')
        # print('翻译后',ts.text)
        if isinstance(ts.text, list):
            for i in ts:
                Data.append(i.text)
            GTransData = Data
        else:
            GTransData = ts.text
        self.trigger.emit()         # 翻译完毕后发出信号
        
import res_rc