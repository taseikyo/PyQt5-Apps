# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mwin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from utils import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

isDown = False # 判断是否正在下载
downloadCount = 0

class Ui_Dialog(QWidget):
    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent)
        self.resize(420, 100)
        self.setMinimumSize(QtCore.QSize(420, 100))
        self.setMaximumSize(QtCore.QSize(420, 100))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.setWindowTitle("进度条")
        self.label.setText("视频下载进度")

class DownloadVideo(QThread): 
    trigger = pyqtSignal()
    status = pyqtSignal()
    def __init__(self, av, src):
        super().__init__()
        self.av = av
        self.src = src
  
    def run(self): 
        global isDown
        global downloadCount
        isDown = True
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
        file_name = self.av + '.flv'
        print("下载", file_name)
        with closing(requests.get(self.src, headers = headers, timeout = 3, stream=True)) as response:  
            print(response.status_code)
            print('headers:', response.headers)
            content_size = int(response.headers['content-length']) # 内容体总大小  
            print('size:', content_size)
            chunk_size = int(content_size/100) # 单次请求最大值 
            print(content_size, chunk_size)
            count = 0
            with open(file_name, "wb") as file:  
                for data in response.iter_content(chunk_size=chunk_size):  
                    file.write(data)
                    count += len(data)
                    self.status.emit()
                    downloadCount = int(count/chunk_size)
                    print(count/chunk_size)
            print("下载完成")
            isDown = False
            self.trigger.emit()         #循环完毕后发出信号
            
class Ui_MWin(object):
    def setupUi(self, MWin):
        MWin.setObjectName("MWin")
        MWin.resize(781, 508)
        MWin.setMinimumSize(QtCore.QSize(781, 508))
        MWin.setMaximumSize(QtCore.QSize(781, 514))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        MWin.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MWin.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MWin)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(30, 30))
        self.tabWidget.setElideMode(QtCore.Qt.ElideRight)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab1)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Layout = QtWidgets.QVBoxLayout()
        self.Layout.setSpacing(10)
        self.Layout.setObjectName("Layout")
        self.Layout_input = QtWidgets.QHBoxLayout()
        self.Layout_input.setSpacing(6)
        self.Layout_input.setObjectName("Layout_input")
        self.lineEdit_input = QtWidgets.QLineEdit(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_input.setFont(font)
        self.lineEdit_input.setInputMask("")
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.Layout_input.addWidget(self.lineEdit_input)
        self.search = QtWidgets.QPushButton(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/b4"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search.setIcon(icon1)
        self.search.setObjectName("search")
        self.Layout_input.addWidget(self.search)
        self.Layout.addLayout(self.Layout_input)
        self.tableWidget = QtWidgets.QTableWidget(self.tab1)
        self.tableWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(7)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(25)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.Layout.addWidget(self.tableWidget)
        self.Layout_download = QtWidgets.QHBoxLayout()
        self.Layout_download.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.Layout_download.setSpacing(6)
        self.Layout_download.setObjectName("Layout_download")
        self.downloadTypes = QtWidgets.QComboBox(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.downloadTypes.setFont(font)
        self.downloadTypes.setObjectName("downloadTypes")
        self.downloadTypes.addItem("")
        self.downloadTypes.addItem("")
        self.downloadTypes.addItem("")
        self.Layout_download.addWidget(self.downloadTypes)
        self.downloadLinks = QtWidgets.QComboBox(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.downloadLinks.setFont(font)
        self.downloadLinks.setObjectName("downloadLinks")
        self.Layout_download.addWidget(self.downloadLinks)
        self.download = QtWidgets.QPushButton(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.download.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/b5"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.download.setIcon(icon2)
        self.download.setObjectName("download")
        self.Layout_download.addWidget(self.download)
        self.Layout_download.setStretch(0, 2)
        self.Layout_download.setStretch(1, 10)
        self.Layout_download.setStretch(2, 2)
        self.Layout.addLayout(self.Layout_download)
        self.Layout.setStretch(0, 1)
        self.Layout.setStretch(1, 7)
        self.horizontalLayout.addLayout(self.Layout)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/b1"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab1, icon3, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab2)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Layout_info = QtWidgets.QVBoxLayout()
        self.Layout_info.setSpacing(6)
        self.Layout_info.setObjectName("Layout_info")
        self.info = QtWidgets.QPlainTextEdit(self.tab2)
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
        self.Layout_info.addWidget(self.info)
        self.verticalLayout_2.addLayout(self.Layout_info)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/b2"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab2, icon4, "")
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab3)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Layout_pay = QtWidgets.QVBoxLayout()
        self.Layout_pay.setSpacing(6)
        self.Layout_pay.setObjectName("Layout_pay")
        self.label_pay = QtWidgets.QLabel(self.tab3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_pay.setFont(font)
        self.label_pay.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pay.setObjectName("label_pay")
        self.Layout_pay.addWidget(self.label_pay)
        self.Layout_2pay = QtWidgets.QHBoxLayout()
        self.Layout_2pay.setSpacing(6)
        self.Layout_2pay.setObjectName("Layout_2pay")
        self.alipay = QtWidgets.QLabel(self.tab3)
        self.alipay.setText("")
        self.alipay.setPixmap(QtGui.QPixmap(":/images/ali"))
        self.alipay.setObjectName("alipay")
        self.Layout_2pay.addWidget(self.alipay)
        self.weicat = QtWidgets.QLabel(self.tab3)
        self.weicat.setText("")
        self.weicat.setPixmap(QtGui.QPixmap(":/images/wecat"))
        self.weicat.setObjectName("weicat")
        self.Layout_2pay.addWidget(self.weicat)
        self.Layout_pay.addLayout(self.Layout_2pay)
        self.Layout_pay.setStretch(0, 1)
        self.Layout_pay.setStretch(1, 5)
        self.verticalLayout_4.addLayout(self.Layout_pay)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/b3"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab3, icon5, "")
        self.verticalLayout.addWidget(self.tabWidget)
        # MWin.setCentralWidget(self.centralWidget)
        # self.statusBar = QtWidgets.QStatusBar(MWin)
        # self.statusBar.setObjectName("statusBar")
        # MWin.setStatusBar(self.statusBar)

        self.retranslateUi(MWin)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MWin)

        self.connectBtn()
        self.cache_index = 0 # 类型下拉框默认是第一个
        self.cover = None # 封面链接
        self.danmu = None # 弹幕链接
        self.av = 0

    def retranslateUi(self, MWin):
        _translate = QtCore.QCoreApplication.translate
        MWin.setWindowTitle(_translate("MWin", "哔哩哔哩工具箱 - ©Tich"))
        self.lineEdit_input.setPlaceholderText(_translate("MWin", "在此输入av号或视频链接"))
        self.lineEdit_input.setFocus()
        self.search.setText(_translate("MWin", "搜索"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MWin", "av号"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MWin", "标题"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MWin", "发布时间"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MWin", "UP主"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MWin", "分类"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MWin", "封面"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MWin", "稿件描述"))
        self.downloadTypes.setItemText(0, _translate("MWin", "视频"))
        self.downloadTypes.setItemText(1, _translate("MWin", "弹幕"))
        self.downloadTypes.setItemText(2, _translate("MWin", "封面"))
        self.download.setText(_translate("MWin", "下载"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("MWin", "首页"))
        self.info.setPlainText(_translate("MWin", "哔哩哔哩工具箱 V1.0\n"
        "主要功能是下载B站视频封面、弹幕和视频源文件\n"
        "没有Cookie下载的是标清的视频\n"
        "若是想下载高清的视频，需要先保存Cookie\n"
        "------\n"
        "GitHub：LewisTian\n"
        "Email：lewissmith@126.com"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MWin", "关于"))
        self.label_pay.setText(_translate("MWin", "若是你觉得好用欢迎投喂ο(=•ω＜=)ρ⌒☆"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("MWin", "投喂"))
        self.search.setShortcut(_translate("MWin", "Ctrl+Return"))

    def connectBtn(self):
        self.search.clicked.connect(self.searchInfo) # 搜索按钮点击事件
        self.downloadTypes.currentIndexChanged.connect(self.downloadTypesChanges) # 类型改变事件
        self.download.clicked.connect(self.downloadMedia) # 搜索按钮点击事件

    def searchInfo(self):
        url = self.lineEdit_input.text()
        # 获取视频信息
        info = get_info(url) # aid,title,pubtime,up,vtype,cover,desc,cid,sex
        if not info:
            return
        # print(info)
        for x in range(len(info)-1):
            item = QTableWidgetItem(info[x])  
            self.tableWidget.setItem(x, 0, item)
        item = QtWidgets.QTableWidgetItem()
        icon = QtGui.QIcon()
        if info[-1] == '女':
            icon.addPixmap(QtGui.QPixmap(":/images/b6"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif info[-1] == '男': 
            icon.addPixmap(QtGui.QPixmap(":/images/b7"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(":/images/b8"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.tableWidget.setItem(3, 0, item)
        item = self.tableWidget.item(3, 0)
        item.setText(info[3])
        self.av = info[0]
        self.cover = info[-4]
        self.danmu = 'https://comment.bilibili.com/{}.xml'.format(info[-2]) # https://comment.bilibili.com/43199797.xml
        print(self.danmu)

        # 获取视频下载信息
        links = get_video_links(self.av)
        # print(links)
        self.downloadLinks.clear()
        if links:
            for x in links:
                self.downloadLinks.addItem(x)

    def downloadTypesChanges(self):
        index = self.downloadTypes.currentIndex()
        if index >= 0 and index != self.cache_index:
            print('currentindex', index)
            self.cache_index = index
            self.downloadLinks.clear()
            if index == 0:
                pass
            elif index == 1:
                print(self.danmu)
                self.downloadLinks.addItem(self.danmu)
            else:
                print(self.cover)
                self.downloadLinks.addItem(self.cover)
            print('count', self.downloadLinks.count())

    def downloadMedia(self):
        count = self.downloadLinks.count()
        if count:
            print("点击下载按钮")
            index = self.downloadTypes.currentIndex()
            if index == 2 or index == 1:
                download_coer_danmu(self.av, self.downloadLinks.itemText(0))
            else:
                if not isDown:
                    src = self.downloadLinks.itemText(self.downloadLinks.currentIndex())
                    av = self.av
                    print(src)
                    # https://stackoverflow.com/questions/15702782/qthread-destroyed-while-thread-is-still-running
                    self.t=DownloadVideo(av, src)
                    self.t.start()
                    self.t.trigger.connect(self.downloaded)
                    self.t.status.connect(self.updateProgress)
                    self.progress = Ui_Dialog()
                    try:
                        with open('style.qss') as f: 
                            style = f.read() # 读取样式表
                            self.progress.setStyleSheet(style)
                    except:
                        print("open stylesheet error")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/images/icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.progress.setWindowIcon(icon)
                    # self.progress.setModal(True)
                    self.progress.show()
                    # download_video(self.av, self.downloadLinks.itemText(self.downloadLinks.currentIndex()))
            # for x in range(count):
            #     print("download", self.downloadLinks.itemText(x))

    def updateProgress(self):
        self.progress.progressBar.setProperty("value", downloadCount)

    def downloaded(self):
        self.progress.close()
        # reply = QMessageBox.about(self, ("哔哩哔哩工具箱 - ©Tich"), (self.av + '.flv'+"视频下载完成"))
        QMessageBox.about(none, ("哔哩哔哩工具箱 - ©Tich"), (self.av + '.flv'+"视频下载完成"))

import res_rc
