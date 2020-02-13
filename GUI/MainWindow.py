# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:MainWindow.py
@time:2018/9/22 15:43
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QDialog, QApplication, QVBoxLayout, QLabel, QWidget

from GUI.ImgPRWidget import ImgPRWidget
from GUI.IndexWidget import IndexWidget
from GUI.SettingWidget import SettingWidget
from GUI.TrainWidget import TrainWidget
from GUI.VideoPRWidget import VideoPRWidget
from prmod.core.CPRecognize import CPRecognize


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.plateRecognize = CPRecognize();

        self.initUI()

    def initUI(self):
        self.resize(600, 500)
        self.setMinimumSize(600, 500)
        self.setStyleSheet('QMainWindow{background-color:white}')
        self.move(int((QApplication.desktop().width() - self.width()) / 2),
                  int((QApplication.desktop().height() - self.height()) / 2))
        self.setWindowTitle('SiriPR')
        self.setWindowIcon(QIcon('GUI/img/icon/siripr_icon_1000_1000.png'))
        self.statusBar().showMessage('Welcome to use SiriPR')

        self.indexWidget = IndexWidget(self)
        self.indexWidget.move(0, 0)

        self.imgPRWidget = ImgPRWidget(self)
        self.imgPRWidget.move(0, 0)
        self.imgPRWidget.hide()

        self.videoPRWidget = VideoPRWidget(self)
        self.videoPRWidget.move(0, 0)
        self.videoPRWidget.hide()

        self.trainWidget = TrainWidget(self)
        self.trainWidget.move(0, 0)
        self.trainWidget.hide()

        self.centerLayout = QVBoxLayout()
        self.centerLayout.addWidget(self.indexWidget)
        self.centerLayout.addWidget(self.imgPRWidget)
        self.centerLayout.addWidget(self.videoPRWidget)
        self.centerLayout.addWidget(self.trainWidget)

        self.centerWidget = QWidget()
        self.centerWidget.setLayout(self.centerLayout)
        self.setCentralWidget(self.centerWidget)

        indexAct = QAction('&Index', self)
        indexAct.setStatusTip('Index page')
        indexAct.triggered.connect(self.on_indexAct_clicked)

        ImgRecognizeAct = QAction('&ImageRecognize', self)
        ImgRecognizeAct.setStatusTip('ImageRecognize')
        ImgRecognizeAct.triggered.connect(self.on_ImgRecognizeAct_clicked)

        ViseoRecognizeAct = QAction('&ViseoRecognize', self)
        ViseoRecognizeAct.setStatusTip('ViseoRecognize')
        ViseoRecognizeAct.triggered.connect(self.on_VideoRecognizeAct_clicked)

        TrainAct = QAction('&Train', self)
        TrainAct.setStatusTip('Train')
        TrainAct.triggered.connect(self.on_TrainAct_clicked)

        settingAct = QAction('&Settings', self)
        settingAct.setStatusTip('Setting config')
        settingAct.triggered.connect(self.on_settingAct_clicked)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        aboutAct = QAction('&About', self)
        aboutAct.setStatusTip('About SiriPR')
        aboutAct.triggered.connect(self.on_aboutAct_clicked)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Main')
        fileMenu.addAction(indexAct)
        fileMenu.addAction(ImgRecognizeAct)
        fileMenu.addAction(ViseoRecognizeAct)
        fileMenu.addAction(TrainAct)
        fileMenu.addSeparator()
        fileMenu.addAction(settingAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAct)

        self.show()

    def on_indexAct_clicked(self):
        self.indexWidget.show()
        self.imgPRWidget.hide()
        self.videoPRWidget.hide()
        self.trainWidget.hide()

    def on_ImgRecognizeAct_clicked(self):
        self.imgPRWidget.show()
        self.indexWidget.hide()
        self.videoPRWidget.hide()
        self.trainWidget.hide()

    def on_VideoRecognizeAct_clicked(self):
        self.videoPRWidget.show()
        self.indexWidget.hide()
        self.imgPRWidget.hide()
        self.trainWidget.hide()

    def on_TrainAct_clicked(self):
        self.trainWidget.show()
        self.indexWidget.hide()
        self.imgPRWidget.hide()
        self.videoPRWidget.hide()

    def on_settingAct_clicked(self):
        settingWidget = SettingWidget(self)

    def on_aboutAct_clicked(self):
        aboutWidget = QDialog(self)
        aboutWidget.setAttribute(Qt.WA_DeleteOnClose)
        aboutWidget.setWindowTitle('About')
        aboutWidget.setStyleSheet('background-color: white;')
        aboutWidget.setFixedSize(350, 450)
        aboutWidget.move(int((QApplication.desktop().width() - aboutWidget.width()) / 2),
                         int((QApplication.desktop().height() - aboutWidget.height()) / 2))

        qimg = QImage('GUI/img/icon/siripr_icon_1000_1000.png').scaled(200, 200)
        imgLabel = QLabel()
        imgLabel.setPixmap(QPixmap.fromImage(qimg))
        imgLabel.setAlignment(Qt.AlignCenter)

        infoLabel = QLabel()
        infoLabel.setFont(QFont("Microsoft YaHei", 12, QFont.Normal))
        infoLabel.setText('SiriPR v1.0\n\n基于 libsiripr 的中国车牌识别系统')
        infoLabel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        buttomLabel = QLabel()
        buttomLabel.setFont(QFont("Microsoft YaHei", 10, QFont.Normal))
        buttomLabel.setText('Copyright © 2020 Siriyang\nblog.siriyang.cn')
        buttomLabel.setAlignment(Qt.AlignCenter| Qt.AlignVCenter)

        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignHCenter)
        vlayout.addWidget(imgLabel)
        vlayout.addWidget(infoLabel)
        vlayout.addWidget(buttomLabel)

        aboutWidget.setLayout(vlayout)
        aboutWidget.exec()
