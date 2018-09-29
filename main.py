# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:main.py
@time:2018/9/22 15:37
"""
import sys

from PyQt5.QtWidgets import QApplication

from GUI.MainWindow import MainWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())