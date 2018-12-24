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
import threading

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

http://moresound.tk/music/api.php?download=bd&74176184=c2b5c49ad319fbada646c34197a5b10e
'''

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
}

with open('Cookie.txt') as f:
	headers['Cookie'] = f.read()

class MWin(QMainWindow, Ui_MWin):
	'''Lossless Music Box'''
	def __init__(self, parent=None):
		super(MWin, self).__init__(parent)
		self.setupUi(self)

		self.midlist = []
		self.setTableHeader = False
		self.text = ''
		self.mtype = -1

		self.iRetrieval = InforRetrieval()
		self.iRetrieval.done.connect(self.resolveInfoDone)
		self.iRetrieval.error.connect(self.errorHappened)

		self.mDownlaod = MusicDonwload()
		self.mDownlaod.error.connect(self.errorHappened)
		self.mDownlaod.done.connect(self.downloadInfoDone)

		self.connectSlots()

	def connectSlots(self):
		'''connect signals with slots functions'''
		self.searchBtn.clicked.connect(self.searchMusic)
		self.downloadBtn.clicked.connect(self.downloadMusic)

	def searchMusic(self):
		text = self.lineEdit.text()
		if not text: return
		mtype = self.comboBox.currentIndex()
		if self.text and self.text == text and self.mtype == mtype:
				return
		self.text = text
		self.mtype = mtype
		self.iRetrieval.w = text
		self.iRetrieval.atype = mtype
		self.iRetrieval.start()

	def downloadMusic(self):
		rows = [x for x in range(self.mtable.rowCount()) if self.mtable.item(x, 0).isSelected()]
		if not rows: return
		self.mDownlaod.num = rows
		self.mDownlaod.mids = [self.midlist[x] for x in rows]
		self.mDownlaod.ftype = [self.mtable.item(x, 1).text() for x in rows]
		# self.mDownlaod.songinfo = [self.mtable.item(x, 2).text() + '-' + self.mtable.item(x, 3).text() for x in rows]
		self.mDownlaod.start()

	def resolveInfoDone(self, info):
		ftype = ['qq', 'kw', 'xm', 'kg', 'bd', 'wy']
		if not self.setTableHeader:
			self.setTableHeader = True
			self.tableHeader = ['#', 'from', 'Song','Singer','Album']
			self.mtable.setColumnCount(len(self.tableHeader))
			self.mtable.setHorizontalHeaderLabels(self.tableHeader)
			self.mtable.horizontalHeader().setVisible(True)
			self.mtable.setColumnWidth(0, 50)
			self.mtable.setColumnWidth(1, 50)
			self.mtable.setColumnWidth(2, 200)
			self.mtable.setColumnWidth(3, 150)
		self.statusBar.showMessage(f'{len(info)} songs find...')
		for x in info:
			row = self.mtable.rowCount()
			self.mtable.insertRow(row)
			self.mtable.setItem(row, 0, QTableWidgetItem(str(row+1)))
			self.mtable.setItem(row, 1, QTableWidgetItem(ftype[x[4]]))
			self.mtable.setItem(row, 2, QTableWidgetItem(x[1]))
			self.mtable.setItem(row, 3, QTableWidgetItem(x[2]))
			self.mtable.setItem(row, 4, QTableWidgetItem(x[3]))
			self.midlist.append(x[0])

	def downloadInfoDone(self, data):
		# header = ['song','singer','album','lrc','cover','url']
		print(data)
		header = ['song','singer','album']
		row = self.dtable.rowCount()
		self.dtable.insertRow(row)
		for i, x in enumerate(header):
			try:
				self.dtable.setItem(row, i, QTableWidgetItem(data[x]))
			except Exception as e:
				pass
		try:
			cover = data['url']['专辑封面']
			self.dtable.setItem(row, i+1, QTableWidgetItem(cover))
		except Exception as e:
			pass
		try:
			lrc = f"http://moresound.tk/music/{data['url']['lrc']}"
			self.dtable.setItem(row, i+2, QTableWidgetItem(lrc))
		except Exception as e:
			pass
		urls = []
		for k, v in data['url'].items():
			if v.find('lrc') > 0 or v.find('jpg') > 0:
				continue
			urls.append(f'http://moresound.tk/music/{v}')
		qcb = QComboBox()
		qcb.addItems(urls)
		self.dtable.setCellWidget(row, 5, qcb)
		if self.tabWidget.currentIndex() != 1:
			self.tabWidget.setCurrentIndex(1)

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
				ret.append([songmid, songname, singer, albumname, self.atype])
		except Exception as e:
			print(e)
			self.error.emit()
			return
		self.done.emit(ret)

class MusicDonwload(QThread):
	'''下载歌曲'''
	done = pyqtSignal(dict)
	error = pyqtSignal()
	def __init__(self):
		super(MusicDonwload, self).__init__()

	def run(self):
		threads = []

		for i, j in enumerate(self.num):
			t = threading.Thread(target=self.getLink, args=(self.mids[i], self.ftype[i]), name=str(j))
			threads.append(t)

		for j in threads:
			j.start()

	def getLink(self, mid, ftype):
		url = f'http://moresound.tk/music/api.php?get_song={ftype}'
		data = {
			'mid': mid
		}
		try:
			r = requests.post(url, headers = headers, data = data).json()
			self.done.emit(r)
		except Exception as e:
			self.error.emit()
		# self.singer = r['singer']
		# self.song = r['song']
		# self.url = r['url']

def main():
	app = QApplication(sys.argv)
	w = MWin()
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
