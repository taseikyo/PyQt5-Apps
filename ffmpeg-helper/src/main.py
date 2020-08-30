#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-19 17:03:07
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : https://github.com/taseikyo
# @Version : Python3.7

import os
import sys
import subprocess

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mwin import Ui_MWin

DURATION_MODE = 0
ENDTIME_MODE = 1

ALLOW_VIDEO_TYPE = [
    "mp4",
    "avi",
    "mkv",
    "ts",
    "rmvb",
    "rm",
    "mov",
]
ALLOW_AUDIO_TYPE = ["m4a", "mp3", "acc", "wav", "flac"]


class MWin(QMainWindow, Ui_MWin):
    def __init__(self, parent=None):
        super(MWin, self).__init__(parent)
        self.setupUi(self)

        self.cut_file_path = ""
        self.merge_files_path = []

        self.merge_video_path = ""
        self.merge_audio_path = ""

        self.mode = DURATION_MODE

        self.cmder_thread = Cmder("")
        self.cmder_thread.log.connect(self.log_display)
        self.cmder_thread.done.connect(self.log_display)
        self.cmder_thread.error.connect(self.error_handler)

        # accept drop event
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        # tab1 and tab2 only accept video while tab3 accepts video and audio
        allow_type = (
            ALLOW_VIDEO_TYPE
            if self.tabWidget.currentIndex() in (0, 1)
            else ALLOW_VIDEO_TYPE + ALLOW_AUDIO_TYPE
        )
        for file in e.mimeData().urls():
            _, ext = os.path.splitext(file.toLocalFile())
            if ext[1:] in allow_type:
                e.accept()
            else:
                e.ignore()

    def dropEvent(self, e):
        # e.mimeData().text() = file:///F:videio/xxx.mp4
        filename = e.mimeData().text()[8:]
        tab_index = self.tabWidget.currentIndex()
        if tab_index == 0:
            # process one file at a time
            self.cut_file_path = filename
            self.filename_label.setText(os.path.basename(filename))
            self.log_edit.setPlainText("")
        elif tab_index == 1:
            # process multiple files at a time
            for file in e.mimeData().urls():
                filename = file.toLocalFile()
                row = self.merge_video_table.rowCount()
                if row == 0:
                    self.merge_video_table.setRowCount(0)
                    self.merge_video_table.setColumnCount(1)
                    self.merge_video_table.setHorizontalHeaderLabels(
                        ["Merge Filenames"]
                    )
                    self.merge_video_table.horizontalHeader().setStretchLastSection(
                        True
                    )
                self.merge_files_path.append(filename)
                self.merge_video_table.insertRow(row)
                self.merge_video_table.setItem(row, 0, QTableWidgetItem(filename))
        else:
            # process one audio and video file at a time
            row = self.merge_va_table.rowCount()
            if row == 0:
                self.merge_va_table.setRowCount(0)
                self.merge_va_table.setColumnCount(1)
                self.merge_va_table.setHorizontalHeaderLabels(["Merge Filenames"])
                self.merge_va_table.horizontalHeader().setStretchLastSection(True)
            self.merge_va_table.insertRow(row)
            self.merge_va_table.setItem(row, 0, QTableWidgetItem(filename))
            _, ext = os.path.splitext(filename)
            if ext[1:] in ALLOW_AUDIO_TYPE:
                self.merge_audio_path = filename
            else:
                self.merge_video_path = filename

    @pyqtSlot()
    def on_select_file_btn_clicked(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "choose file", "", "*")
        if not filename:
            return

        self.cut_file_path = filename
        self.filename_label.setText(os.path.basename(filename))
        self.log_edit.setPlainText("")

    def on_duration_check_stateChanged(self, mode):
        if mode == 0:
            self.mode = ENDTIME_MODE
            self.radio_label.setText("End Time:")
        else:
            self.mode = DURATION_MODE
            self.radio_label.setText("Duration:")

    @pyqtSlot()
    def on_start_btn_clicked(self):
        if not self.cut_file_path:
            return

        start_offset_raw = (
            self.start_time_edit.text().replace("：", ":").replace(" ", "")
        )
        end_offset_raw = self.end_time_edit.text().replace("：", ":").replace(" ", "")

        start_offset = self.time_format_check(start_offset_raw)
        end_offset = self.time_format_check(end_offset_raw)

        self.start_time_edit.setText(start_offset)
        self.end_time_edit.setText(end_offset)

        if (not start_offset) or (not end_offset):
            return

        tmp = os.path.splitext(self.cut_file_path)
        out_file = f"{tmp[0]}_cut{tmp[1]}"

        if self.mode == ENDTIME_MODE:
            if not self.time_interval_check(start_offset, end_offset):
                return

            cmd = f'ffmpeg -i "{self.cut_file_path}" -vcodec copy -acodec copy -ss {start_offset} -to {end_offset} "{out_file}" -y'
        else:
            cmd = f'ffmpeg -ss {start_offset} -i "{self.cut_file_path}" -vcodec copy -acodec copy -t {end_offset} "{out_file}" -y'

        self.cmder_thread.cmd = cmd
        self.cmder_thread.start()

    @pyqtSlot()
    def on_extract_btn_clicked(self):
        if not self.cut_file_path:
            return

        name, _ = os.path.splitext(self.cut_file_path)
        cmd = f'''ffmpeg -i "{self.cut_file_path}" -vn -y -acodec copy "{name}.m4a"'''
        self.cmder_thread.cmd = cmd
        self.cmder_thread.start()

    def time_format_check(self, time_raw):
        """check `time_raw` is legal
        and return a legal time
        """
        time_legal = []
        carry = 0
        for x in time_raw.split(":")[::-1]:
            try:
                tmp = int(x) + carry
                if tmp > 59:
                    carry = tmp // 60
                    tmp %= 60
                time_legal.append(str(tmp))
            except:
                return ""
        if carry:
            time_legal.append(str(carry))
        return ":".join(time_legal[::-1])

    def time_interval_check(self, time_start, time_end):
        """check end > start
        """
        start, end = 0, 0
        base = 1
        for x in time_start.split(":")[::-1]:
            start += base * int(x)
            base *= 10
        base = 1
        for x in time_end.split(":")[::-1]:
            end += base * int(x)
            base *= 10
        return start < end

    @pyqtSlot()
    def on_select_video_files_btn_clicked(self):
        files, ok = QFileDialog.getOpenFileNames(
            self, "choose file", "", "MP4 Files (*.mp4)"
        )
        if not ok:
            return
        self.merge_files_path = files

        self.merge_video_table.clearContents()
        self.merge_video_table.setRowCount(0)
        self.merge_video_table.setColumnCount(1)
        self.merge_video_table.setHorizontalHeaderLabels(["Merge Filenames"])
        self.merge_video_table.horizontalHeader().setStretchLastSection(True)

        for x in range(len(files)):
            self.merge_video_table.insertRow(x)
            print(files[x])
            self.merge_video_table.setItem(x, 0, QTableWidgetItem(files[x]))

    @pyqtSlot()
    def on_clear_video_files_btn_clicked(self):
        self.merge_files_path = []

        self.merge_video_table.clearContents()
        self.merge_video_table.setRowCount(0)
        self.merge_video_table.setColumnCount(1)
        self.merge_video_table.setHorizontalHeaderLabels(["Merge Filenames"])
        self.merge_video_table.horizontalHeader().setStretchLastSection(True)

    @pyqtSlot()
    def on_start_merge_video_btn_clicked(self):
        if not self.merge_files_path or len(self.merge_files_path) < 2:
            return

        ts_files = []
        out_dir = os.path.split(self.merge_files_path[0])[0]
        # transform
        for x in self.merge_files_path:
            out_file, _ = os.path.splitext(x)
            ts_files.append(f"{out_file}.ts")
            cmd = f'ffmpeg -i "{x}" -acodec copy -vcodec copy -absf aac_adtstoasc -y "{out_file}.ts"'
            try:
                with os.popen(cmd) as f:
                    print(f.read())
            except Exception as e:
                print(e)
                return

        cwd = os.getcwd()
        os.chdir(out_dir)
        # merge
        cmd = f'''ffmpeg -i "concat:{'|'.join(ts_files)}" -acodec copy -vcodec copy -absf aac_adtstoasc -y "{ts_files[0]}_merge.mp4"'''
        print(cmd)
        try:
            with os.popen(cmd) as f:
                print(f.read())
        except Exception as e:
            print(e)
            os.remove(f"{ts_files[0]}_merge.mp4")
            return

        for x in ts_files:
            os.remove(x)

        os.chdir(cwd)

    def log_display(self, text):
        old_text = self.log_edit.toPlainText()
        self.log_edit.setPlainText(f"{old_text}{text}")

        scrollbar = self.log_edit.verticalScrollBar()
        if scrollbar:
            scrollbar.setSliderPosition(scrollbar.maximum())

    def error_handler(self, emsg):
        QMessageBox.warning(self, "FFmpeg Helper", emsg, QMessageBox.Ok)

    @pyqtSlot()
    def on_select_va_files_btn_clicked(self):
        files, ok = QFileDialog.getOpenFileNames(self, "choose file", "", "*")
        if not ok:
            return

        self.merge_video_path = ""
        self.merge_audio_path = ""

        self.merge_va_table.clearContents()
        self.merge_va_table.setRowCount(0)
        self.merge_va_table.setColumnCount(1)
        self.merge_va_table.setHorizontalHeaderLabels(["Merge Filenames"])
        self.merge_va_table.horizontalHeader().setStretchLastSection(True)

        for x in range(len(files)):
            self.merge_va_table.insertRow(x)
            print(files[x])
            self.merge_va_table.setItem(x, 0, QTableWidgetItem(files[x]))

    @pyqtSlot()
    def on_clear_va_files_btn_clicked(self):
        self.merge_video_path = ""
        self.merge_audio_path = ""

        self.merge_va_table.clearContents()
        self.merge_va_table.setRowCount(0)
        self.merge_va_table.setColumnCount(1)
        self.merge_va_table.setHorizontalHeaderLabels(["Merge Filenames"])
        self.merge_va_table.horizontalHeader().setStretchLastSection(True)

    @pyqtSlot()
    def on_start_merge_va_btn_clicked(self):
        if self.merge_va_table.rowCount() < 2:
            return

        if self.merge_video_path and self.merge_audio_path:
            self.merge_video_audio()

        for x in range(self.merge_va_table.rowCount()):
            file = self.merge_va_table.item(x, 0).text()
            _, ext = os.path.splitext(file)
            if ext[1:] in ALLOW_AUDIO_TYPE:
                self.merge_audio_path = file
            elif ext[1:] in ALLOW_VIDEO_TYPE:
                self.merge_video_path = file

            if self.merge_video_path and self.merge_audio_path:
                self.merge_video_audio()
                break

    def merge_video_audio(self):
        cmd = f'''mp4box.exe -add "{self.merge_video_path}#trackID=1:name=" -add "{self.merge_audio_path}#trackID=1:name=" -new "{self.merge_video_path}_merge.mp4"'''
        print(cmd)
        try:
            with os.popen(cmd) as f:
                print(f.read())
        except Exception as e:
            print(e)
            os.remove(f"{self.merge_video_path}_merge.mp4")
            return


class Cmder(QThread):
    log = pyqtSignal(str)
    error = pyqtSignal(str)
    done = pyqtSignal(str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        try:
            p = subprocess.Popen(
                self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            for line in iter(p.stdout.readline, b""):
                try:
                    line = line.decode("utf-8")
                except:
                    line = line.decode("gbk")
                self.log.emit(line)
        except Exception as e:
            self.error.emit(str(e))
        self.done.emit("done")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MWin()
    w.show()
    sys.exit(app.exec_())
