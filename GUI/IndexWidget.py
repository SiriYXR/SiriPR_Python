# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:IndexWidget.py
@time:2018/9/24 16:41
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel


class IndexWidget(QWidget):

    def __init__(self, fWind):
        super().__init__()

        self.fWindow = fWind

        self.initUI()

    def initUI(self):
        self.label_center = QLabel()
        self.label_center.setMinimumSize(300, 300)
        self.label_center.setMaximumSize(1024, 720)
        self.label_center.resize(400, 400)

        self.btn_ImgRecognize = QPushButton("ImageRecognize")
        self.btn_ImgRecognize.setMaximumSize(1000, 1000)
        self.btn_ImgRecognize.setStyleSheet('')
        self.btn_ImgRecognize.setStatusTip('Image recognize')
        self.btn_ImgRecognize.clicked.connect(self.on_btn_ImgRecognize_clicked)

        self.btn_VideoRecognize = QPushButton("VideoRecognize")
        self.btn_VideoRecognize.setMaximumSize(1000, 1000)
        self.btn_VideoRecognize.setStatusTip('Video recognize')
        self.btn_VideoRecognize.clicked.connect(self.on_btn_VideoRecognize_clicked)

        self.btn_Train = QPushButton("Train")
        self.btn_Train.setMaximumSize(1000, 1000)
        self.btn_Train.setStatusTip('Train model')
        self.btn_Train.clicked.connect(self.on_btn_Train_clicked)

        self.btn_Settings = QPushButton("Settings")
        self.btn_Settings.setMaximumSize(1000, 1000)
        self.btn_Settings.setStatusTip('Settings')
        self.btn_Settings.clicked.connect(self.on_btn_Settings_clicked)

        self.btn_About = QPushButton("About")
        self.btn_About.setMaximumSize(1000, 1000)
        self.btn_About.setStatusTip('About SiriPR')
        self.btn_About.clicked.connect(self.on_btn_About_clicked)

        self.layout_Recognize = QVBoxLayout()
        self.layout_Recognize.addWidget(self.btn_ImgRecognize)
        self.layout_Recognize.setStretchFactor(self.btn_ImgRecognize, 1)
        self.layout_Recognize.addWidget(self.btn_VideoRecognize)
        self.layout_Recognize.setStretchFactor(self.btn_VideoRecognize, 1)

        self.layout_Train = QVBoxLayout()
        self.layout_Train.addWidget(self.btn_Train)

        self.layout_Function = QHBoxLayout()
        self.layout_Function.addLayout(self.layout_Recognize)
        self.layout_Function.setStretchFactor(self.layout_Recognize, 2)
        self.layout_Function.addLayout(self.layout_Train)
        self.layout_Function.setStretchFactor(self.layout_Train, 1)

        self.layout_Others = QHBoxLayout()
        self.layout_Others.addWidget(self.btn_Settings)
        self.layout_Others.setStretchFactor(self.btn_Settings, 5)
        self.layout_Others.addWidget(self.btn_About)
        self.layout_Others.setStretchFactor(self.btn_About, 1)

        self.cLaout = QVBoxLayout()
        self.cLaout.addLayout(self.layout_Function)
        self.cLaout.setStretchFactor(self.layout_Function, 4)
        self.cLaout.addLayout(self.layout_Others)
        self.cLaout.setStretchFactor(self.layout_Others, 1)

        self.label_center.setLayout(self.cLaout)

        self.vLaout = QVBoxLayout()
        self.vLaout.addWidget(self.label_center)
        self.vLaout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.vLaout)

    def on_btn_ImgRecognize_clicked(self):
        self.fWindow.on_ImgRecognizeAct_clicked()

    def on_btn_VideoRecognize_clicked(self):
        self.fWindow.on_VideoRecognizeAct_clicked()

    def on_btn_Train_clicked(self):
        self.fWindow.on_TrainAct_clicked()

    def on_btn_Settings_clicked(self):
        self.fWindow.on_settingAct_clicked()

    def on_btn_About_clicked(self):
        self.fWindow.on_aboutAct_clicked()
