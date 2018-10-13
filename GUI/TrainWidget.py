# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:TrainWidget.py
@time:2018/9/26 12:50
"""
import threading
import time

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget

from prmod.train.SVM_train_Thread import SVM_train_Thread
from prmod.util.Utiles import stop_thread


class TrainWidget(QWidget):

    def __init__(self, fwind):
        super().__init__()

        self.fWindow = fwind
        self.svmthread=SVM_train_Thread()

        self.initUI()

    def initUI(self):
        """-------------------- topLayout------------------------"""
        self.btn_return = QPushButton("<-")
        self.btn_return.setFixedSize(30, 30)
        self.btn_return.setStatusTip("Return index page")
        self.btn_return.clicked.connect(self.on_btn_return_clicked)

        self.label_RunningMSG = QLabel()
        self.label_RunningMSG.setAlignment(Qt.AlignCenter)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.btn_return)
        self.topLayout.addWidget(self.label_RunningMSG)

        """--------------------------------------------"""

        self.btn_train=QPushButton("train")
        self.btn_train.clicked.connect(self.on_btn_train_clicked)


        """-------------------- vlayout------------------------"""
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.topLayout)
        self.vlayout.addWidget(self.btn_train)

        self.vlayout.setAlignment(Qt.AlignTop)

        self.setLayout(self.vlayout)

    @pyqtSlot(bool)
    def on_btn_return_clicked(self, checked):
        self.fWindow.on_indexAct_clicked()

    @pyqtSlot(bool)
    def on_btn_train_clicked(self, checked):

        self.svmthread.start()
        time.sleep(5)
        stop_thread(self.svmthread)


    def keyPressEvent(self, event):

        key=event.key()

        if key==Qt.Key_Escape:
            self.fWindow.on_indexAct_clicked()
            return

        super().keyPressEvent(event)