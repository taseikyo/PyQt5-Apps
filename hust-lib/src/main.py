#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-20 16:44:42
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mwin import Ui_MWin
from bs4 import BeautifulSoup as Soup
import threading
import requests

class MWin(QMainWindow, Ui_MWin):
	def __init__(self, parent=None):
		super(MWin, self).__init__(parent)
		self.setupUi(self)

		# 实例化状态栏，设置状态栏
		self.statusBar = QStatusBar()
		self.setStatusBar(self.statusBar)


		# 'http://ftp.lib.hust.edu.cn' + pre + '/' page*50+1 + suf
		self.pre = ''
		self.suf = ''
		self.cur_page = 1
		self.total_pages = 1
		self.cur_row = 0
		self.first_kw = True

		self.book_lists = [] # 获取的图书表数据：书名 简介 链接

		self.request = Request('LewisTian', 1, '', '', 1) # kw p pre suf flag
		self.request.done.connect(self.resolveDataDone)
		self.request.error.connect(self.errorHappened)
		self.request.detail_done.connect(self.detailDone)
		
		self.table_has_header = False

		self.connectSlots()

	def connectSlots(self):
		self.search_btn.clicked.connect(self.resolveInput)
		# 跳转
		self.pre_page_btn.clicked.connect(lambda: self.retrievePage(-1))
		self.next_page_btn.clicked.connect(lambda: self.retrievePage(-2))
		self.last_page_btn.clicked.connect(lambda: self.retrievePage(-3))
		self.jump_page_btn.clicked.connect(lambda: self.retrievePage(self.jump_page.value()))

		self.table.cellDoubleClicked.connect(self.bookDetails)

	def resolveInput(self):
		'''get input keyword and search books'''
		kw = self.keyword.text()
		if not kw: return

		self.first_kw = True
		self.cur_page = 1

		self.request.kw = kw
		self.request.flag = 1
		self.request.start()
		self.statusBar.showMessage('正在搜索中...', 3000)

	def retrievePage(self, page):
		if page == self.cur_page:
			return
		elif page == -1:
			if self.cur_page == 1: return
			self.cur_page -= 1
		elif page == -2:
			if self.cur_page == self.total_pages: return
			self.cur_page += 1
		elif page == -3:
			if self.cur_page == self.total_pages: return
			self.cur_page = self.total_pages
		else:
			self.cur_page = page
		
		self.request.p = self.cur_page
		self.request.flag = 1
		self.request.start()
		self.statusBar.showMessage('正在搜索中...', 3000)

	def resolveDataDone(self, data):
		self.statusBar.showMessage('搜索结束...', 1000)

		if self.first_kw:
			self.total_pages = int(data[0])
			self.jump_page.setMaximum(self.total_pages)
			self.page_count.setText(f'一共 {self.total_pages} 页')
			self.first_kw = False
			
		self.current_page_index.setText(f'当前 {self.cur_page} 页')
		self.jump_page.setValue(self.cur_page)
		self.pre = data[1]
		self.suf = data[2]
		self.request.pre = self.pre
		self.request.suf = self.suf

		books = data[-1]

		if not self.table_has_header:
			self.table.setColumnCount(2)
			self.table.setHorizontalHeaderLabels(['书名', '本书简介'])
			self.table_has_header = True

		else:
			self.table.clearContents()
			self.table.setRowCount(0)

		lists = []
		for x in books:
			tl = x.find('span', {'class', 'briefcitTitle'}).a
			title = tl.text
			link = tl['href']
			detail = x.find('span', {'class', 'briefcitDetail'}).text.replace('\n', ' ')
			lists.append([title, detail, link])
			row = self.table.rowCount()
			self.table.insertRow(row)
			self.table.setItem(row, 0, QTableWidgetItem(title))
			self.table.setItem(row, 1, QTableWidgetItem(detail))
		self.book_lists = lists

	def bookDetails(self, row, col):
		self.request.flag = 0
		self.cur_row = row
		self.statusBar.showMessage(f'正在获取{self.book_lists[row][0]}的信息...', 3000)
		self.request.run(self.book_lists[row][-1])

	def detailDone(self, data):
		book = self.book_lists[self.cur_row][0]
		QMessageBox.information(self, '华中科技大学图书馆公共查询系统', f'{book}\n\n{data}', QMessageBox.Ok)

	def errorHappened(self, msg):
		QMessageBox.warning(self, '华中科技大学图书馆公共查询系统', msg, QMessageBox.Ok)

class Request(QThread):
	done = pyqtSignal(list) # num pre suf books
	detail_done = pyqtSignal(str)
	error = pyqtSignal(str)
	def __init__(self, kw, p, pre, suf, flag):
		super(Request, self).__init__()
		self.kw = kw
		self.p = p
		self.pre = pre
		self.suf = suf
		self.flag = flag # 1: books 0: details
		self.headers = {
			'Host': 'ftp.lib.hust.edu.cn',
			'Referer': 'http://www.lib.hust.edu.cn/',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
		}

	def run(self, link = None):
		if self.flag:
			self.books()
		else:
			self.detail(link)

	def books(self):
		p = self.p
		data = []
		if p <= 1:
			url = f'http://ftp.lib.hust.edu.cn/search*chx/X?SEARCH={self.kw}'
		else:
			url = f'http://ftp.lib.hust.edu.cn{self.pre}/{(p-1)*50+1}{self.suf}'
		try:
			r = requests.get(url, headers = self.headers)
			soup = Soup(r.text, 'html5lib')
			table = soup.find('table', {'calss', 'browseScreen'})
			pages = table.find('tr', {'class', 'browsePager'})
		except:
			self.error.emit('未找到该书的信息...')
			return
		if not pages:
			QDesktopServices.openUrl(QUrl(f'http://ftp.lib.hust.edu.cn/search*chx/X?SEARCH={self.kw}'))
			return
		last_page = pages.find_all('a')[-2]
		link = last_page['href'] 
		num = last_page.text
		pre, suf = re.findall(r'(.*?SUBKEY=.*?)/\d+(%2C.*?/browse)', link)[0]
		books = table.find_all('td', {'class', 'briefCitRow'})
		data = [num, pre, suf, books]
		self.done.emit(data)

	def detail(self, link):
		url = f'http://ftp.lib.hust.edu.cn{link}'
		try:
			r = requests.get(url, headers = self.headers)
			soup = Soup(r.text, 'html5lib')
			info = soup.find_all('tr', {'calss', 'bibItemsEntry'})
		except:
			self.error.emit('未找到该书的信息...')
			return
		ret = '\n'.join([x.text.replace('\n', '') for x in info])
		self.detail_done.emit(ret)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = MWin()
	w.show()
	sys.exit(app.exec_())
