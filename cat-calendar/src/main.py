#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-21 14:16:48
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import sys
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
from PIL import Image, ImageDraw, ImageFont

from mwin import Ui_MWin

BASE = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']

class MWin(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MWin, self).__init__(parent)
        self.setupUi(self)

        if not os.path.exists('images'):
            os.mkdir('images')

        self.bn_image = 'default.png'
        self.bg_color = '#f0f0f0'
        self.font_path = 'Microsoft YaHei Mono.ttf'

    @pyqtSlot()
    def on_banner_image_btn_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select banner image', '', 'images(*.png; *.jpg);;*')
        if file[0]:
            self.bn_image = file[0]
        else:
            self.bn_image = 'default.png'
        self.banner_image.setText(f'Banner image (1: 1) {os.path.basename(self.bn_image)}')

    @pyqtSlot()
    def on_background_color_btn_clicked(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.bg_color = f'#{hex(col.red())[2:]}{hex(col.green())[2:]}{hex(col.blue())[2:]}'
        else:
            self.bg_color = '#f0f0f0'
        self.background_color.setText(f'Background color: {self.bg_color}')

    @pyqtSlot()
    def on_font_btn_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Select fonts', '', 'fonts(*.ttf; *.otf);;*')
        if file[0]:
            self.font_path = file[0]
        else:
            self.font_path = 'Microsoft YaHei Mono.ttf'
        self.font.setText(f'Font: {os.path.basename(self.font_path)}')

    @pyqtSlot()
    def on_start_btn_clicked(self):
        self.render_image()

    @pyqtSlot()
    def on_open_btn_clicked(self):
        QDesktopServices.openUrl(QUrl('images'))

    def error(self, msg):
        QMessageBox.information(self, 'Cat Calendar', msg, QMessageBox.Ok)

    def render_image(self):
        banner_path = self.bn_image
        bg_color = self.bg_color
        font = self.font_path
        inner_color = '#fff'
        text_color = ['#000', '#515151', '#8d8d8d']

        w, h = 1080, 1920
        outter_padding = 30
        inner_padding = 20
        bn_w = w - (outter_padding + inner_padding) * 2
        line_space = 30

        banner = Image.open(banner_path)
        # 1: 1 banner image required
        if banner.size[0] != banner.size[1]:
            self.error('Image size must be 1: 1!')
            return

        banner = banner.resize((bn_w, bn_w), resample=3)

        out_img = Image.new(mode='RGB', size=(w, h), color=bg_color)
        draw = ImageDraw.Draw(out_img)

        # draw inner background
        # radius
        r = 15
        x = y = outter_padding
        draw.ellipse((x, y, x+r*2, y+r*2), fill=inner_color)
        draw.ellipse((w-x-r*2, y, w-x, y+r*2), fill=inner_color)
        draw.ellipse((x, h-y-r*2, x+r*2, h-y), fill=inner_color)
        draw.ellipse((w-x-r*2, h-y-r*2, w-x, h-y), fill=inner_color)
        draw.rectangle((x, y+r, w-x, h-y-r), fill=inner_color)
        draw.rectangle((x+r, y, w-x-r, h-y), fill=inner_color)

        # paste banner
        out_img.paste(banner, (outter_padding+inner_padding, outter_padding+inner_padding))

        # text
        small_font_size = 30
        font_size = 45
        big_font_size = 140
        shift = 5
        normal_font = ImageFont.truetype(font, font_size)
        big_font = ImageFont.truetype(font, big_font_size)
        small_font = ImageFont.truetype(font, small_font_size)

        date = datetime.datetime.now() # Sunday-Saturday
        date_w, date_h = ImageDraw.Draw(Image.new(mode='RGB',
                                                  size=(1, 1))).textsize(str(date.day), font=big_font)
        y = outter_padding+inner_padding*3+bn_w
        draw.text(((w-date_w)//2, y), str(date.day), font=big_font, fill=text_color[1])

        today = BASE[date.weekday()] if date.weekday() != 6 else '日'
        text = f'星期{today} {date.month}月'
        date_w, date_h1 = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(text, font=normal_font)
        y += inner_padding+date_h+shift
        draw.text(((w-date_w)//2, y), text, font=normal_font, fill=text_color[2])

        y += inner_padding+date_h1+shift
        draw.line(((w-date_w)//2, y) + ((w+date_w)//2, y), fill=text_color[2])

        url = f'http://www.dutangapp.cn/u/toxic?date={date.strftime("%Y-%m-%d")}'
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
            text = r.json()['data'][0]['data']
        except:
            text = '只要你坚持不懈的，去追你喜欢的人，总有一天你会被他拉黑。'

        date_w, date_h2 = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(text, font=normal_font)

        if date_w > 930:
            table = {ord(f): ord(t) for f, t in zip(u'，。', u',.')}
            text = text.translate(table).replace(',', '\n').replace('.', '')
            date_w, date_h2 = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(text, font=normal_font)
        # one/dutang text
        y += inner_padding+shift*3
        draw.text((outter_padding+inner_padding*2, y), text, font=normal_font, fill=text_color[1], spacing=line_space)

        y += date_h2+len(text.split('\n'))*line_space
        text = '来源：毒汤日历'
        date_w, _ = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(text, font=small_font)
        draw.text((w-date_w-inner_padding-outter_padding, y), text, font=small_font, fill=text_color[2])

        text = 'rendered by Cat Calendar'
        date_w, date_h = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(text, font=small_font)
        draw.text(((w-date_w)//2, h-outter_padding-date_h), text, font=small_font, fill=text_color[0])


        name, ext = os.path.basename(banner_path).split('.')
        out_img.save(f'images/{name}_cat.{ext}')
        self.error(f'image rendered at images/{name}_cat.{ext}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MWin()
    w.show()
    sys.exit(app.exec_())