#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-28 15:41:05
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mwin import Ui_MWin
import jieba
from wordcloud import WordCloud
from imageio import imread

class MWin(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MWin, self).__init__(parent)
        self.setupUi(self)

        self.groupBox_4.setHidden(True)

        self.words = '' # input words
        self.stopwords = f'{os.path.split(os.path.realpath(__file__))[0]}/stopwords.txt'
        self.bgc = '#fff' # background color
        self.bgi = '' # background image
        self.font = f'{os.path.split(os.path.realpath(__file__))[0]}/SourceHanSansCN-Bold.otf'

        self.w = Generator(self.words,self.stopwords,self.bgc,self.font,self.bgi)
        self.w.done.connect(self.done)
        self.w.error.connect(self.error)

        if not os.path.exists('images'):
            os.mkdir('images')

    def resizeEvent(self, event):
        if self.size().height() > 550:
            self.groupBox_4.setHidden(False)
        else:
            self.groupBox_4.setHidden(True)

    @pyqtSlot()
    def on_text_btn_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select files','','text files(*.txt)')
        if file[0]:
            self.words = file[0]
            self.text_label.setText(self.words.split('/')[-1])
            self.text_label.setToolTip(self.words.split('/')[-1])

    @pyqtSlot()
    def on_stop_btn_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select files','','text files(*.txt)')
        if file[0]:
            self.stopwords = file[0]
            self.stop_label.setText(self.stopwords.split('/')[-1])
            self.stop_label.setToolTip(self.stopwords.split('/')[-1])

    @pyqtSlot()
    def on_color_btn_clicked(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.bgc = col.name()
            self.color_label.setStyleSheet('QLabel {background-color:%s}' % col.name())
            self.color_label.setToolTip(col.name())

    @pyqtSlot()
    def on_bgi_btn_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select images','','images(*.png; *.jpg; *.jpeg)')
        if file[0]:
            self.bgi = file[0]
            self.bgi_label.setText(self.bgi.split('/')[-1])
            self.bgi_label.setToolTip(self.bgi.split('/')[-1])

    @pyqtSlot()
    def on_font_btn_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select fonts','','fonts(*.ttf; *.otf);;*')
        if file[0]:
            self.font = file[0]
            self.font_label.setText(self.font.split('/')[-1])
            self.font_label.setToolTip(self.font.split('/')[-1])


    @pyqtSlot()
    def on_open_btn_clicked(self):
        QDesktopServices.openUrl(QUrl('images'))

    @pyqtSlot()
    def on_start_btn_clicked(self):
        if not self.words: return
        self.w.words = self.words
        self.w.stopwords = self.stopwords
        self.w.color = self.bgc
        self.w.image = self.bgi
        self.w.font = self.font
        self.w.start()

    def done(self):
        QMessageBox.information(self, '词云图生成器', '词云图生成完毕！', QMessageBox.Ok)

    def error(self, msg):
        QMessageBox.information(self, '词云图生成器', msg, QMessageBox.Ok)

class Generator(QThread):
    done = pyqtSignal()
    error = pyqtSignal(str)
    def __init__(self, words, stopwords, color, font, image=None):
        super(Generator, self).__init__()
        self.words = words
        self.stopwords = stopwords
        self.color = color
        self.font = font
        self.image = image

    def run(self):
        with open(self.stopwords, encoding='utf-8') as f_stop:
            f_stop_text = f_stop.read()
            f_stop_seg_list = f_stop_text.splitlines()

        # 读入文本内容
        text = open(self.words, encoding='utf-8').read()

        # 中文分词
        seg_list = jieba.cut(text, cut_all=False)

        # 把文本中的stopword剃掉
        my_word_list = []

        for my_word in seg_list:
            if len(my_word.strip()) > 1 and not (my_word.strip() in f_stop_seg_list):
                my_word_list.append(my_word)

        my_word_str = ' '.join(my_word_list)
        
        # 字体不要包含中文，否则会报错！
        font_path = self.font
        
        if self.image:
            wc = WordCloud(
                font_path=font_path,
                background_color=self.color,
                mask=imread(self.image),
            )
        else:
            wc = WordCloud(
                font_path=font_path,
                background_color=self.color,
                random_state=1024,
                width=1920,
                height=1080,
            )
        try:
            wc.generate(my_word_str)
            wc.to_file('images/wordcloud.png')
            self.done.emit()
        except Exception as e:
            self.error.emit(str(e))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MWin()
    w.show()
    sys.exit(app.exec_())
