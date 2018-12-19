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
import requests
import sys
import re

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

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': 'Tip_of_the_day=2; encrypt_data=9393b2797f6b8514fcea144aef4a15e5973a3643e8584ab6e2f82e34ef050ffb53caae316abcc67a9b08a21e3b5334d9c96d04ddb6c41119a77628d2256376aa878dc4a0c79b9226b811497da1b8389ba4bfdf4bc2f61eddb9e7a9f04fe0fa69d5d99dc65cd353d0e00e8855e6d64efb4b45b7a20599950e24d05bfc1ef8738d',
}

class MWin(QMainWindow, Ui_MWin):
	'''Lossless Music Box'''
	def __init__(self, parent=None):
		super(MWin, self).__init__(parent)
		self.setupUi(self)

		self.midlist = []

		self.iRetrieval = InforRetrieval()
		self.iRetrieval.done.connect(self.resolveInfoDone)
		self.iRetrieval.error.connect(self.errorHappened)

		self.connectSlots()
		

	def connectSlots(self):
		'''connect signals with slots functions'''
		self.searchBtn.clicked.connect(self.searchMusic)

	def searchMusic(self):
		text = self.lineEdit.text()
		if not text: return
		self.iRetrieval.w = text
		self.iRetrieval.atype = self.comboBox.currentIndex()
		self.iRetrieval.start()

	def resolveInfoDone(self, info):
		self.tableHeader = ['#','Song','Singer','Album']
		self.mtable.setColumnCount(len(self.tableHeader))
		self.mtable.setHorizontalHeaderLabels(self.tableHeader)
		self.mtable.horizontalHeader().setVisible(True)
		self.mtable.setColumnWidth(0, 50)
		self.mtable.setColumnWidth(1, 150)
		self.mtable.setColumnWidth(2, 150)
		for x in info:
			row = self.mtable.rowCount()
			self.mtable.insertRow(row)
			self.mtable.setItem(row, 0, QTableWidgetItem(str(row+1)))
			self.mtable.setItem(row, 1, QTableWidgetItem(x[1]))
			self.mtable.setItem(row, 2, QTableWidgetItem(x[2]))
			self.mtable.setItem(row, 3, QTableWidgetItem(x[3]))
			self.midlist.append(x[0])

	def errorHappened(self, msg = 'an error accrued...'):
		QMessageBox.warning(self, 'Lossless Music Box v1.0.0 ©Lewis Tian', msg, QMessageBox.Ok)

class InforRetrieval(QThread):
	'''获取收藏信息'''
	done = pyqtSignal(list)
	error = pyqtSignal()
	def __init__(self):
		super(InforRetrieval, self).__init__()

	def run(self):
		typeList = ['qq', 'kw', 'xm', 'kg', 'bd', 'wy']
		
		data = {
			'p': 1,
			'w': self.w,
			'n': 20
		}
		url = f'http://moresound.tk/music/api.php?search={typeList[self.atype]}'
		ret = []
		try:
			r = requests.post(url, data = data, headers = headers).json()
			totalnum = r['totalnum']
			data = r['song_list']
			for x in data:
				songmid = x['songmid']
				songname = x['songname'].replace('\n', '').replace(' ', '')
				songname = re.sub('<.*>', '', songname)
				if len(x['singer']) > 1:
					singer = ' - '.join([i['name'] for i in x['singer']])
				else:
					singer = x['singer'][0]['name']
				albumname = x['albumname']
				ret.append([songmid, songname, singer, albumname])
		except Exception as e:
			print(e)
			self.error.emit()
			return
		self.done.emit(ret)

def main():
	app = QApplication(sys.argv)
	w = MWin()
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
