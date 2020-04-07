# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:ImgFileWidget.py
@time:2020/4/7 11:47
"""

import os
import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton

MAIN_STYLE="""
        *{
            background-color:#fff;
        }
        
        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:dimgray;
            background-color:#fff;
            border:0px solid #B5ADAD;
            border-radius:2px;
            text-align: center;
        }
        QPushButton:hover
        {
            color:#fff;
            background-color:dimgray;
        }
        QPushButton:pressed
        {
            color:#fff;
            background-color:dimgray;
            padding-left:3px;
            padding-top:3px;
        }
        
        """

class ImgFileWidget(QWidget):

    def __init__(self, fWind,path):
        super().__init__()
        self.fWindow=fWind

        self.config = configparser.ConfigParser()

        self.file_path=""
        self.file_name=""
        self.plates=[]

        self.debug_value = False
        self.label_value = False
        self.detecttype_value = 0
        self.maxplates_value =1

        self.loadData(path)
        self.initUI()


    def loadData(self,path):
        self.file_path=path
        self.file_name=os.path.basename(path)
        self.plates=[]

        self.config.read("resources/config/siripr.ini")

        self.debug_value=(self.config.get('VIDEOPR', 'debug') == 'True')
        self.label_value=(self.config.get('VIDEOPR', 'label') == 'True')
        self.detecttype_value=int(self.config.get('VIDEOPR', 'detecttype'))
        self.maxplates_value=int(self.config.get('VIDEOPR', 'maxplates'))

    def initUI(self):
        self.setFixedHeight(25)
        self.setStyleSheet(MAIN_STYLE)

        self.checkBox=QCheckBox()
        self.checkBox.setFixedSize(15,25)
        self.checkBox.setTristate(False) # 取消半选中状态
        self.checkBox.clicked.connect(self.fWindow.updateCheckedList)

        self.fileNameBtn=QPushButton(self.file_name)
        self.fileNameBtn.setFixedHeight(25)
        self.fileNameBtn.clicked.connect(self.showImg)

        layout=QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.fileNameBtn)

        self.setLayout(layout)

    def showImg(self):
        self.fWindow.showImageFile(self.file_path)