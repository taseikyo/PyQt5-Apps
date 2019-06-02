#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-13 15:24:23
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io/
# @Version : Python3.6

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication, QTimer, QDateTime, Qt
from mwin import Ui_MWin
import sys
import re
import pymysql
from configparser import ConfigParser

# global val
status = "logged in: %s, lasted: %s."
db = None
cursor = None
outSql = """
SELECT * FROM words INTO OUTFILE '%s' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
"""
inSql = """
INSERT INTO words(origin, trans) VALUES (%s, %s);
"""

class MainWindow(QMainWindow):
    def closeEvent(self, event):
        if db:
            db.close()

    def messageBox(self, showInfo):
        """:author : Tich
        show information."""
        box = QMessageBox.about(self, 'Words Recoder 1.0', showInfo)

    def importData(self, w):
        """:author : Tich
        import data via file.
        the file consists of two columns,
        one for words and one for translation
        there is a '\n' in the last line
        """
        if db:
            filename, filetype = QFileDialog.getOpenFileName(None, 'Open File', '.')
            data = []
            if filename:
                print(filename)
                with open(filename, encoding = 'utf-8') as f:
                    for x in f:
                        words = re.split(r'\s+', x[:-1])
                        if len(words) == 2:
                            data.append(words)
                print(data)
            try:
                flag = cursor.executemany(inSql, data)
                if flag:
                    db.commit()
                    self.messageBox("data has been imported!")
                    self.updateTable(w)
            except Exception as e:
                db.rollback()
                self.messageBox("import data failed!\nerror msg: %s"%(e.args[1]))
        else:
            self.messageBox("connect to the database first!\nclick the button 'File-connect'")

    def exportDataAsCSV(self):
        # filename, filetype = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '.', "All Files (*);;Text Files (*.txt)")
        if db:
            filename, filetype = QFileDialog.getSaveFileName(None, 'Save File', self.outPath, "CSV Files (*.csv)")
            if filename:
                print(filename)
                try:
                    num = cursor.execute(outSql % filename)
                    if num:
                        # self.messageBox("data has been exported as %s", % (filename) )
                        self.messageBox("data has been exported as %s!" % filename)
                except Exception as e:
                    self.messageBox("export data failed!\nerror msg: %s"%(e.args[1]))
        else:
            self.messageBox("connect to the database first!\nclick the button 'File-connect'")

    def connectDatabase(self, w):
        """:author : Tich
        connect to database
        :param w: used for data update in `w.table`
        """
        global db, cursor
        if db:
            return
        config = ConfigParser()
        conf = {}
        try:
            config.readfp(open('setting.ini'))
            head = ['host', 'user', 'password', 'db', 'port', 'charset', 'path']
            for x in head:
                conf[x] = config.get("MySQL", x)
            self.outPath = conf['path']
        except:
           self.messageBox("config the 'setting.ini' file first!")
           return
        try:
            # print(conf)
            # db = pymysql.connect(conf)
            db = pymysql.connect(host=conf['host'],user=conf['user'],password=conf['password'],
                db=conf['db'],port=int(conf['port']), charset=conf['charset'])
            cursor = db.cursor()
            self.messageBox("connected to the database!\nthe table will be updated.")
        except Exception as e:
            self.messageBox("database connect error!\nerror msg: %s.\
                    \n===\nplease check your databse setting \nand restart the app."%(e.args[1]))
            return
        # update data once connecting to the database
        self.updateTable(w)

    def updateTable(self, w):
        """:author : Tich
        update data in the table
        :param w: update data in `w.table`
        """
        try:
            num = cursor.execute("SELECT * FROM words ORDER BY origin;")
            if num:
                w.table.setRowCount(num)
                for r in cursor:
                    # print(r)
                    i = cursor.rownumber - 1
                    for x in range(3):
                        item = QTableWidgetItem(str(r[x]))
                        item.setTextAlignment(Qt.AlignCenter);
                        w.table.setItem(i, x, item)
        except Exception as e:
            # print(e)
            self.messageBox("update table error!\nerror msg: %s"%e.args[1])

    def insert(self, w):
        origin = w.input_origin.text().replace(' ', '')
        trans = w.input_trans.text().replace(' ', '')
        if origin and trans:
            if db:
                try:
                    sql = "INSERT INTO words(origin, trans) VALUES ('%s', '%s');" %(origin, trans)
                    print(sql)
                    num = cursor.execute(sql)
                    if num:
                        db.commit()
                        # self.messageBox("data has been inserted!")
                        self.updateTable(w)
                except Exception as e:
                    db.rollback()
                    self.messageBox("insert data failed!\nerror msg: %s"%(e.args[1]))
            else:
                self.messageBox("connect to the database first!\nclick the button 'File-connect'")

    def query(self, w):
        origin = w.input_origin.text().replace(' ', '')
        if origin:
            if db:
                try:
                    sql = "SELECT origin, trans FROM words WHERE origin = '%s'" % origin
                    print(sql)
                    num = cursor.execute(sql)
                    if num:
                        for r in cursor:
                            w.input_trans.setText(r[1])
                            # self.messageBox("%s: %s"%(r))
                except Exception as e:
                    self.messageBox("insert data failed!\nerror msg: %s"%(e.args[1]))
            else:
                self.messageBox("connect to the database first!\nclick the button 'File-connect'")

    def update(self, w):
        flag = False
        if db:
            for x in w.table.selectedIndexes():
                sql = "update words set origin='%s', trans='%s' where id=%s;"
                print(w.table.item(x.row(), 1).text())
                num = cursor.execute(sql%(w.table.item(x.row(), 1).text(), w.table.item(x.row(), 2).text(), w.table.item(x.row(), 0).text()))
                if num:
                    flag = True
                    db.commit()
                else:
                    pass
                # print(x.row())
                # w.table.item(i,j)
            if flag:
                self.updateTable(w)
        else:
            self.messageBox("connect to the database first!\nclick the button 'File-connect'")

    def delete(self, w):
        flag = False
        if db:
            for x in w.table.selectedIndexes():
                sql = "delete from words where Id = '%s';"
                num = cursor.execute(sql % w.table.item(x.row(), 0).text())
                if num:
                    flag = True
                    db.commit()
                else:
                    pass
            if flag:
                self.updateTable(w)
        else:
            self.messageBox("connect to the database first!\nclick the button 'File-connect'")

def connectSlots(base, w):
    """:author : Tich
    connect w with base slots
    """
    # close event
    w.actionexit.triggered.connect(base.close)
    # about
    w.actionabout.triggered.connect(lambda: base.messageBox("Words Recoder 1.0: Recod unknown words into the MySQL database."))
    # heko
    w.actionhelp.triggered.connect(lambda: base.messageBox("1.click 'File - connect' to connect MySQL.\
                                                                                               \n2. click button 'insert' to insert new word. \
                                                                                              \n3. click button 'query' to query word."))
    # import data via file
    w.actionimport.triggered.connect(lambda: base.importData(w)) 
    # export data as .csv file
    w.actionexport.triggered.connect(base.exportDataAsCSV) 
    # connect to MySQL
    w.actionconnect.triggered.connect(lambda: base.connectDatabase(w)) 

    w.insert.clicked.connect(lambda: base.insert(w))
    w.insert.setShortcut('Ctrl+Return')

    w.query.clicked.connect(lambda: base.query(w))
    w.query.setShortcut('Ctrl+Q')

    w.update.clicked.connect(lambda: base.update(w))
    w.update.setShortcut('Ctrl+U')

    w.delet.clicked.connect(lambda: base.delete(w))
    w.delet.setShortcut('Ctrl+D')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = MainWindow() # create base window
    try:
        with open('style.qss') as f: 
            style = f.read() # 读取样式表
            base.setStyleSheet(style)
    except:
        print("open stylesheet error")
    w = Ui_MWin() # create user ubterface instance
    w.setupUi(base) # load w into base window
    w.table.setColumnWidth(0, 40) 
    connectSlots(base, w)
    base.show() # show base window
    sys.exit(app.exec_())
