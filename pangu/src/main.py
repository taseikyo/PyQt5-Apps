#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-09 15:09:09
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.8


import os
import sys

import pangu
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mwin import Ui_MWin

CHARS = [
    ("（", "("),
    ("）", ")"),
    ("。", "."),
    ("，", ","),
    ("；", ";"),
    ("：", ":"),
    ("〉", ">"),
    ("〈", "<"),
    ("！", "!"),
]


class MWin(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MWin, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pangu_btn_clicked(self):
        text = self.before_txt.toPlainText()
        if text:
            text = self.handle_text(text)

            try:
                text = pangu.spacing_text(text)
            except:
                pass

            self.after_txt.setText(text)

    @pyqtSlot()
    def on_copy_btn_clicked(self):
        text = self.after_txt.toPlainText()
        if text:
            QApplication.clipboard().setText(text)

    def onClipboradChanged(self):
        """
        根据是否 `监听剪贴板` 和 `自动替换回车`
        """
        if not self.listen_clip_board.isChecked():
            return

        clipboard = QApplication.clipboard()
        text = clipboard.text()

        if not text:
            return

        text = self.handle_text(text)

        self.before_txt.setText(text)

        try:
            text = pangu.spacing_text(text)
        except:
            pass

        self.after_txt.setText(text)

    def handle_text(self, text):
        """
        在外层已经确保 @text 不会空，所以不需要判断
        """
        if self.remove_newline.isChecked():
            text = text.replace("\n", " ")

        if self.replace_symbol.isChecked():
            for k, v in CHARS:
                text = text.replace(k, v)

        return text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MWin()
    w.show()
    clipboard = QApplication.clipboard()
    clipboard.dataChanged.connect(w.onClipboradChanged)
    sys.exit(app.exec_())
