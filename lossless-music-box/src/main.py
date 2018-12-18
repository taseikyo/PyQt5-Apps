#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-18 21:47:15
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mwin import Ui_MWin
import sys

'''
API
===
get songlist:
url: http://moresound.tk/music/api.php?search=qq
method: POST
data: 	w: key word
		p: page
		n: song num per page (20 default)
		
---
get song detail:
url: http://moresound.tk/music/api.php?get_song=qq
method: POST
data: mid
'''

class MWin(QMainWindow, Ui_MWin):
	'''Lossless Music Box'''
	def __init__(self, parent=None):
		super(MWin, self).__init__(parent)
		self.setupUi(self)

def main():
	app = QApplication(sys.argv)
	w = MWin()
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
