#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-16 15:39:02
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io/
# @Version : Python3.6

from mwin import Ui_MWin

from PyQt5.QtCore import QTranslator, QUrl, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QDesktopServices, QPixmap
import sys
from googletrans import Translator
import re

GTransData = ""


class MyWindow(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        try:
            with open("style.qss") as f:
                style = f.read()  # 读取样式表
                self.setStyleSheet(style)
        except:
            print("open stylesheet error")
        self.originText.setFocus(True)
        #  Translator
        self.trans = QTranslator()
        # destination language
        self.dest = "zh-CN"
        # ui language : 0->zh-CN, 1->en
        self.lan = 0
        # real-time translate
        self.isRealTimeTrans = False
        self.isCopyFromTrans = False
        self.connectSlots()

    def connectSlots(self):
        self.alwaysFront.clicked.connect(self.alwaysFrontFunc)  # windows top
        self.realTimeTrans.clicked.connect(
            self.realTimeTransFunc
        )  # real-time translate

        self.go.clicked.connect(self.transTextToZhCN)
        self.go.setShortcut("CTRL+Return")

        self.copy.clicked.connect(self.copySlot)

        # connect to slots
        self.openFile.triggered.connect(self.openFileSlot)
        self.exportFile.triggered.connect(self.exportFileSlot)
        self.exit.triggered.connect(self.close)

        self.actionChinese.triggered.connect(lambda: self.changeLanguage(0))
        self.actionEnglish.triggered.connect(lambda: self.changeLanguage(1))

        self.actionDestChinese.triggered.connect(lambda: self.destinationLanguage(0))
        self.actionDestEnglish.triggered.connect(lambda: self.destinationLanguage(1))
        self.actionDestJapanese.triggered.connect(lambda: self.destinationLanguage(2))
        self.actionDestKorean.triggered.connect(lambda: self.destinationLanguage(3))

        self.about.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl(
                    "https://github.com/taseikyo/PyQt5-Apps/tree/master/google-translate"
                )
            )
        )
        self.about.setShortcut("CTRL+H")
        self.donate.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/taseikyo/PyQt5-Apps#donation")
            )
        )
        self.reportBug.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/taseikyo/PyQt5-Apps/issues")
            )
        )

    def openFileSlot(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "Open File", ".")
        if filename:
            print(filename)
            with open(filename, encoding="utf-8") as f:
                try:
                    self.originText.setPlainText(str(f.read()))
                except Exception as e:
                    self.originText.setPlainText(e.args[1])

    def exportFileSlot(self):
        if not self.transText.toPlainText():
            return
        filename, filetype = QFileDialog.getSaveFileName(
            self, "Save File", ".", "*.txt;;*"
        )
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                try:
                    f.write(self.transText.toPlainText())
                except Exception as e:
                    self.transText.setPlainText(e.args[1])

    def changeLanguage(self, lan):
        """:author : Tich
        :param lan: 0=>Chinese, 1=>English
        change ui language
        """
        if lan == 0 and self.lan != 0:
            self.lan = 0
            print("[MainWindow] Change to zh_CN")
            self.trans.load("zh_CN")
        elif lan == 1 and self.lan != 1:
            self.lan = 1
            print("[MainWindow] Change to English")
            self.trans.load("en")
        else:
            return
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)

    def destinationLanguage(self, lan):
        """:author : Tich
        :param lan: 0: Chinese, 1: English, 2: Japanese, 3: Korean
        change destination language
        """
        if lan == 0:
            self.dest = "zh-CN"
        elif lan == 1:
            self.dest = "en"
        elif lan == 2:
            self.dest = "ja"
        elif lan == 3:
            self.dest = "ko"
        else:
            self.dest = "en"
        print(self.dest)

    def transTextToZhCN(self):
        text = self.originText.toPlainText()
        if text:
            if (
                self.paperMode.isChecked()
            ):  # if paper mode is true, line breaks will re replaced by blanks
                text = re.sub(r"\n|\s+", " ", text)
                text = re.sub(r"", "", text)
                # add on 19/05/16
                text = (
                    text.replace("", "fi")
                    .replace("", "ffi")
                    .replace("", "ff")
                    .replace("", "fl")
                    .replace("", "th")
                    .replace("", "ft")
                    .replace("", "ft")
                    .replace("", "tt")
                )
            self.originText.setPlainText(text)
            try:
                # self.transText.setPlainText(trans_To_zh_CN(text))
                self.t = GTranslator(self.dest, text)
                self.t.start()
                self.transText.setPlainText("")
                self.transText.setPlaceholderText("...")
                self.t.trigger.connect(self.translated)
            except Exception as e:
                print(e.args[1])
                self.transText.setPlainText("error!")

    def translated(self):
        global GTransData
        if GTransData:
            self.transText.setPlainText(GTransData)
        else:
            self.transText.setPlainText("error!")
        GTransData = ""

    def alwaysFrontFunc(self):
        """change window status
        """
        if self.alwaysFront.isChecked():
            # print("Front", self.windowFlags())
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowStaysOnTopHint
            )  # always top
            self.show()
        else:
            # print("Back", self.win.windowFlags())
            self.setWindowFlags(Qt.Widget)
            self.show()

    def realTimeTransFunc(self):
        """real-time translate
        this fearure is for paper mode
        """
        # print(self.isRealTimeTrans)
        self.isRealTimeTrans = self.realTimeTrans.isChecked()

    def copySlot(self):
        s = self.transText.toPlainText()
        if s:
            self.isCopyFromTrans = True
            clipboard = QApplication.clipboard()
            clipboard.setText(s)

    def onClipboradChanged(self):
        if self.isCopyFromTrans:
            self.isCopyFromTrans = False
            return
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text and self.isRealTimeTrans:
            content = str(text)
            # print(content)
            content = (
                content.replace("", "fi")
                .replace("", "ffi")
                .replace("", "ff")
                .replace("", "fl")
                .replace("", "th")
                .replace("", "ft")
                .replace("", "ft")
                .replace("", "tt")
            )
            if (
                self.paperMode.isChecked()
            ):  # if paper mode is true, line breaks will re replaced by blanks
                content = re.sub(r"\n|\s+", " ", content)
                content = re.sub(r"", "", content)
            self.originText.setPlainText(content)
            self.transText.setPlainText(content)
            try:
                # data = trans_To_zh_CN(content)
                # self.transText.setPlainText(data)
                self.t = GTranslator(self.dest, content)
                self.t.start()
                self.transText.setPlainText("")
                self.transText.setPlaceholderText("...")
                self.t.trigger.connect(self.translated)
            except:
                self.transText.setPlainText("error!")


class GTranslator(QThread):
    trigger = pyqtSignal()

    def __init__(self, dest, content):
        super().__init__()
        self.content = content
        self.dest = dest

    def run(self):
        Data = []
        global GTransData
        T = Translator(service_urls=["translate.google.cn"])
        # ts = T.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='zh-CN')
        try:
            ts = T.translate(self.content, dest=self.dest)
            if isinstance(ts.text, list):
                for i in ts:
                    Data.append(i.text)
                GTransData = Data
            else:
                GTransData = ts.text
        except:
            GTransData = "An error happended. Please retry..."
        self.trigger.emit()  # emit signal once translatation is finfished


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    clipboard = QApplication.clipboard()
    clipboard.dataChanged.connect(w.onClipboradChanged)
    sys.exit(app.exec_())
