# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:MainWindow.py
@time:2020/4/5 15:56
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QDialog, QApplication, QVBoxLayout,QHBoxLayout, QLabel, QWidget ,QPushButton

from GUI2.ImgPRWidget import ImgPRWidget
from GUI2.SettingWidget import SettingWidget
from GUI2.VideoPRWidget import VideoPRWidget
from prmod.core.CPRecognize import CPRecognize


TOP_BTN_ON_STYLE="""
        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:#27a2f1;
            background-color:#f1f1f1;
            border-radius:0px;
        }

        QPushButton:hover
        {
            background-color:#f1f1f1;
        }

        QPushButton:pressed
        {
            background-color:#f1f1f1;
            padding-left:3px;
            padding-top:3px;
        }
        """

TOP_BTN_OFF_STYLE="""
        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:#8e8e8e;
            background-color:#f1f1f1;
            border-radius:0px;
        }

        QPushButton:hover
        {
            background-color:#f1f1f1;
        }

        QPushButton:pressed
        {
            background-color:#f1f1f1;
            padding-left:3px;
            padding-top:3px;
        }
        """

MAINWINDOW_STYL="""
        *{
            font-family:Microsoft Yahei;
            font-size:12px;
            color:dimgray;
        }
        QMainWindow{
            background-color:#FBFAFA
        }
        QMenuBar{
            font-family:Microsoft Yahei;
            font-size:12px;
            color:dimgray;
        }
        """

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.plateRecognize = CPRecognize();

        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setStyleSheet(MAINWINDOW_STYL)
        self.move(int((QApplication.desktop().width() - self.width()) / 2),
                  int((QApplication.desktop().height() - self.height()) / 2))
        self.setWindowTitle('SiriPR')
        self.setWindowIcon(QIcon('GUI2/img/icon/siripr_icon_1000_1000.png'))
        self.statusBar().showMessage('欢迎使用SiriPR')

        self.imgPRBtn = QPushButton('图像识别')
        self.imgPRBtn.setFixedHeight(30)
        self.imgPRBtn.setStyleSheet(TOP_BTN_ON_STYLE)
        self.imgPRBtn.setStatusTip('图像识别')
        self.imgPRBtn.clicked.connect(self.on_ImgRecognizeAct_clicked)

        self.videoPRBtn = QPushButton('视频识别')
        self.videoPRBtn.setFixedHeight(30)
        self.videoPRBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.videoPRBtn.setStatusTip('视频识别')
        self.videoPRBtn.clicked.connect(self.on_VideoRecognizeAct_clicked)

        self.settingBtn = QPushButton('系统设置')
        self.settingBtn.setFixedHeight(30)
        self.settingBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.settingBtn.setStatusTip('系统设置')
        self.settingBtn.clicked.connect(self.on_SettingAct_clicked)

        self.topLayout = QHBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)
        self.topLayout.setSpacing(0)
        self.topLayout.addWidget(self.imgPRBtn)
        self.topLayout.addWidget(self.videoPRBtn)
        self.topLayout.addWidget(self.settingBtn)

        self.imgPRWidget = ImgPRWidget(self)
        self.imgPRWidget.move(0, 0)
        self.imgPRWidget.hide()

        self.videoPRWidget = VideoPRWidget(self)
        self.videoPRWidget.move(0, 0)
        self.videoPRWidget.hide()

        self.settingWidget = SettingWidget(self)
        self.settingWidget.move(0, 0)
        self.settingWidget.hide()

        self.bottomLayout = QVBoxLayout()
        self.bottomLayout.addWidget(self.imgPRWidget)
        self.bottomLayout.addWidget(self.videoPRWidget)
        self.bottomLayout.addWidget(self.settingWidget)

        self.centerLayout = QVBoxLayout()
        self.centerLayout.setContentsMargins(0,0,0,0)
        self.centerLayout.setSpacing(5)
        self.centerLayout.addLayout(self.topLayout)
        self.centerLayout.addLayout(self.bottomLayout)

        self.centerWidget = QWidget()
        self.centerWidget.setLayout(self.centerLayout)
        self.setCentralWidget(self.centerWidget)

        ImgRecognizeAct = QAction('&图片识别', self)
        ImgRecognizeAct.setStatusTip('图片识别')
        ImgRecognizeAct.triggered.connect(self.on_ImgRecognizeAct_clicked)

        ViseoRecognizeAct = QAction('&视频识别', self)
        ViseoRecognizeAct.setStatusTip('视频识别')
        ViseoRecognizeAct.triggered.connect(self.on_VideoRecognizeAct_clicked)

        settingAct = QAction('&系统设置', self)
        settingAct.setStatusTip('系统设置')
        settingAct.triggered.connect(self.on_SettingAct_clicked)

        exitAct = QAction('&退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('退出应用')
        exitAct.triggered.connect(qApp.quit)

        aboutAct = QAction('&关于', self)
        aboutAct.setStatusTip('关于SiriPR')
        aboutAct.triggered.connect(self.on_AboutAct_clicked)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&主菜单')
        fileMenu.addAction(ImgRecognizeAct)
        fileMenu.addAction(ViseoRecognizeAct)
        fileMenu.addSeparator()
        fileMenu.addAction(settingAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&帮助')
        helpMenu.addAction(aboutAct)

        self.imgPRWidget.show()
        self.videoPRWidget.hide()
        self.settingWidget.hide()
        self.show()

    def on_ImgRecognizeAct_clicked(self):
        self.imgPRWidget.show()
        self.videoPRWidget.hide()
        self.settingWidget.hide()

        self.imgPRBtn.setStyleSheet(TOP_BTN_ON_STYLE)
        self.videoPRBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.settingBtn.setStyleSheet(TOP_BTN_OFF_STYLE)

    def on_VideoRecognizeAct_clicked(self):
        self.videoPRWidget.show()
        self.imgPRWidget.hide()
        self.settingWidget.hide()

        self.imgPRBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.videoPRBtn.setStyleSheet(TOP_BTN_ON_STYLE)
        self.settingBtn.setStyleSheet(TOP_BTN_OFF_STYLE)

    def on_SettingAct_clicked(self):
        self.videoPRWidget.hide()
        self.imgPRWidget.hide()
        self.settingWidget.show()

        self.imgPRBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.videoPRBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.settingBtn.setStyleSheet(TOP_BTN_ON_STYLE)

    def on_AboutAct_clicked(self):
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
