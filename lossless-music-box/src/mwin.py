# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mwin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MWin(object):
    def setupUi(self, MWin):
        MWin.setObjectName("MWin")
        MWin.resize(720, 400)
        MWin.setMinimumSize(QtCore.QSize(720, 400))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(11)
        MWin.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/music-box.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MWin.setWindowIcon(icon)
        MWin.setIconSize(QtCore.QSize(40, 40))
        self.centralWidget = QtWidgets.QWidget(MWin)
        self.centralWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(8, 10, 8, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.searchBtn = QtWidgets.QToolButton(self.centralWidget)
        self.searchBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchBtn.setObjectName("searchBtn")
        self.horizontalLayout.addWidget(self.searchBtn)
        self.downloadBtn = QtWidgets.QToolButton(self.centralWidget)
        self.downloadBtn.setEnabled(False)
        self.downloadBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadBtn.setObjectName("downloadBtn")
        self.horizontalLayout.addWidget(self.downloadBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.mtable = QtWidgets.QTableWidget(self.centralWidget)
        self.mtable.setAlternatingRowColors(True)
        self.mtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.mtable.setObjectName("mtable")
        self.mtable.setColumnCount(0)
        self.mtable.setRowCount(0)
        self.verticalLayout.addWidget(self.mtable)
        MWin.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MWin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 720, 26))
        self.menuBar.setObjectName("menuBar")
        MWin.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MWin)
        self.statusBar.setObjectName("statusBar")
        MWin.setStatusBar(self.statusBar)

        self.retranslateUi(MWin)
        QtCore.QMetaObject.connectSlotsByName(MWin)

    def retranslateUi(self, MWin):
        _translate = QtCore.QCoreApplication.translate
        MWin.setWindowTitle(_translate("MWin", "Lossless Music Box v1.0.0 ©Lewis Tian"))
        self.comboBox.setItemText(0, _translate("MWin", "QQ"))
        self.comboBox.setItemText(1, _translate("MWin", "酷我"))
        self.comboBox.setItemText(2, _translate("MWin", "虾米"))
        self.comboBox.setItemText(3, _translate("MWin", "酷狗"))
        self.comboBox.setItemText(4, _translate("MWin", "百度"))
        self.comboBox.setItemText(5, _translate("MWin", "网易"))
        self.searchBtn.setText(_translate("MWin", "Search"))
        self.downloadBtn.setText(_translate("MWin", "Download"))

import res_rc
