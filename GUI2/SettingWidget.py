# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:SettingWidget.py
@time:2020/4/5 15:59
"""

import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFileDialog, \
    QPushButton, QScrollArea,QGridLayout

BTN_STYLE="""
        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:dimgray;
            background-color:#fff;
            border:1px solid #B5ADAD;
            border-radius:2px;
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

SCROLLAREA_STYLE="""
        QLabel{
            font-family:Microsoft Yahei;
            font-size:14px;
            color:dimgray;
            font-weight:bold;
        }
        QWidget{
            background:#fff;
        }
        QLineEdit{
            border:1px solid #B5ADAD;
            font-family:Microsoft Yahei;
            font-size:13px;
            color:gray;
        }
        QScrollArea{
            border:0px solid #B5ADAD;
        }
        QScrollBar:vertical  
        {
            border-radius:7px;  
            background:#f1f1f1; 
            padding-top:14px;  
            padding-bottom:14px;  
        }
        QScrollBar::handle:vertical
        {
            background:#C4CAD0; 
            border-radius:6px;  
            margin-left:2px;  
            margin-right:2px;  
        }
        QScrollBar::handle:vertical:hover  
        {
            background:gray;
            border-radius:6px;
        }
        QScrollBar::add-line:vertical  
        {
            height:14px;width:8px;  
            image:url('');  
        }
        QScrollBar::sub-line:vertical  
        {
            height:14px;width:8px;
            image:url('');  
        }
        QScrollBar::add-line:vertical:hover  
        {
            height:14px;width:8px;
            image:url('');
            subcontrol-position:bottom;
        }
        QScrollBar::sub-line:vertical:hover 
        {
            height:14px;width:8px;
            image:url('');  
            subcontrol-position:top;
        }
        QScrollBar::add-page:vertical  
        {
            background:#f1f1f1;
        }
        QScrollBar::sub-page:vertical  
        {
            background:#f1f1f1; 
        }
        """

class SettingWidget(QWidget):

    def __init__(self, fWind):
        super().__init__(fWind)
        self.fWindow=fWind

        self.config = configparser.ConfigParser()

        self.config.read("resources/config/siripr.ini")

        self.initUI()
        self.resetData()

    def initUI(self):

        self.label_ModelPath=QLabel('模型路径设置')
        self.label_ModelPath.setFixedHeight(20)
        self.label_ModelPath.setAlignment(Qt.AlignCenter)

        self.label_SVM = QLabel('SVM模型路径:')
        self.label_SVM.setFixedSize(200,20)
        self.label_SVM.setAlignment(Qt.AlignLeft)
        self.lineedit_SVM = QLineEdit()
        self.lineedit_SVM.setFixedHeight(30)
        self.btn_SVM = QPushButton('...')
        self.btn_SVM.setStyleSheet(BTN_STYLE)
        self.btn_SVM.setFixedSize(30,30)
        self.btn_SVM.clicked.connect(self.on_btn_SVM_clicked)

        layout_SVM = QGridLayout()
        layout_SVM.setContentsMargins(0, 5, 0, 0)
        layout_SVM.setSpacing(5)
        layout_SVM.addWidget(self.label_SVM,0,0)
        layout_SVM.addWidget(self.lineedit_SVM,1,0)
        layout_SVM.addWidget(self.btn_SVM,1,1)

        self.label_ANN = QLabel('ANN模型路径:')
        self.label_ANN.setFixedSize(200,20)
        self.label_ANN.setAlignment(Qt.AlignLeft)
        self.lineedit_ANN = QLineEdit()
        self.lineedit_ANN.setFixedHeight(30)
        self.btn_ANN = QPushButton('...')
        self.btn_ANN.setStyleSheet(BTN_STYLE)
        self.btn_ANN.setFixedSize(30,30)
        self.btn_ANN.clicked.connect(self.on_btn_ANN_clicked)

        layout_ANN = QGridLayout()
        layout_ANN.setContentsMargins(0, 5, 0, 0)
        layout_ANN.setSpacing(5)
        layout_ANN.addWidget(self.label_ANN,0,0)
        layout_ANN.addWidget(self.lineedit_ANN,1,0)
        layout_ANN.addWidget(self.btn_ANN,1,1)

        self.label_ChineseANN = QLabel('ChineseANN模型路径:')
        self.label_ChineseANN.setFixedSize(200,20)
        self.label_ChineseANN.setAlignment(Qt.AlignLeft)
        self.lineedit_ChineseANN = QLineEdit()
        self.lineedit_ChineseANN.setFixedHeight(30)
        self.btn_ChineseANN = QPushButton('...')
        self.btn_ChineseANN.setStyleSheet(BTN_STYLE)
        self.btn_ChineseANN.setFixedSize(30,30)
        self.btn_ChineseANN.clicked.connect(self.on_btn_ChineseANN_clicked)

        layout_ChineseANN = QGridLayout()
        layout_ChineseANN.setContentsMargins(0, 5, 0, 0)
        layout_ChineseANN.setSpacing(5)
        layout_ChineseANN.addWidget(self.label_ChineseANN,0,0)
        layout_ChineseANN.addWidget(self.lineedit_ChineseANN,1,0)
        layout_ChineseANN.addWidget(self.btn_ChineseANN,1,1)

        self.label_GrayChANN = QLabel('GrayChANN模型路径:')
        self.label_GrayChANN.setFixedSize(200,20)
        self.label_GrayChANN.setAlignment(Qt.AlignLeft)
        self.lineedit_GrayChANN = QLineEdit()
        self.lineedit_GrayChANN.setFixedHeight(30)
        self.btn_GrayChANN = QPushButton('...')
        self.btn_GrayChANN.setStyleSheet(BTN_STYLE)
        self.btn_GrayChANN.setFixedSize(30,30)
        self.btn_GrayChANN.clicked.connect(self.on_btn_GrayChANN_clicked)

        layout_GrayChANN = QGridLayout()
        layout_GrayChANN.setContentsMargins(0, 5, 0, 0)
        layout_GrayChANN.setSpacing(5)
        layout_GrayChANN.addWidget(self.label_GrayChANN,0,0)
        layout_GrayChANN.addWidget(self.lineedit_GrayChANN,1,0)
        layout_GrayChANN.addWidget(self.btn_GrayChANN,1,1)

        self.label_ChineseMapping = QLabel('ChineseMapping文件路径:')
        self.label_ChineseMapping.setFixedSize(200,20)
        self.label_ChineseMapping.setAlignment(Qt.AlignLeft)
        self.lineedit_ChineseMapping = QLineEdit()
        self.lineedit_ChineseMapping.setFixedHeight(30)
        self.btn_ChineseMapping = QPushButton('...')
        self.btn_ChineseMapping.setStyleSheet(BTN_STYLE)
        self.btn_ChineseMapping.setFixedSize(30,30)
        self.btn_ChineseMapping.clicked.connect(self.on_btn_ChineseMapping_clicked)

        layout_ChineseMapping = QGridLayout()
        layout_ChineseMapping.setContentsMargins(0, 5, 0, 0)
        layout_ChineseMapping.setSpacing(5)
        layout_ChineseMapping.addWidget(self.label_ChineseMapping,0,0)
        layout_ChineseMapping.addWidget(self.lineedit_ChineseMapping,1,0)
        layout_ChineseMapping.addWidget(self.btn_ChineseMapping,1,1)

        layout_ModelPath=QVBoxLayout()
        layout_ModelPath.setContentsMargins(5, 10, 5, 0)
        layout_ModelPath.setSpacing(10)
        layout_ModelPath.addWidget(self.label_ModelPath)
        layout_ModelPath.addLayout(layout_SVM)
        layout_ModelPath.addLayout(layout_ANN)
        layout_ModelPath.addLayout(layout_ChineseANN)
        layout_ModelPath.addLayout(layout_GrayChANN)
        layout_ModelPath.addLayout(layout_ChineseMapping)
        layout_ModelPath.addStretch()

        self.sa_contentWidget = QWidget()
        self.sa_contentWidget.setFixedSize(600, 1000)
        self.sa_contentWidget.setLayout(layout_ModelPath)

        self.sa_Settings = QScrollArea()
        self.sa_Settings.setStyleSheet(SCROLLAREA_STYLE)
        self.sa_Settings.setWidget(self.sa_contentWidget)
        self.sa_Settings.setAlignment(Qt.AlignHCenter)

#------------------------------------------------------
        self.btn_defualt = QPushButton('默认')
        self.btn_defualt.setFixedSize(60,30)
        self.btn_defualt.setStyleSheet(BTN_STYLE)
        self.btn_defualt.setStatusTip('恢复默认设置')
        self.btn_defualt.clicked.connect(self.on_btn_defualt_clicked)
        self.btn_cancel = QPushButton('取消')
        self.btn_cancel.setFixedSize(60, 30)
        self.btn_cancel.setStyleSheet(BTN_STYLE)
        self.btn_cancel.setStatusTip('取消未保存的修改')
        self.btn_cancel.clicked.connect(self.on_btn_cancel_clicked)
        self.btn_apply = QPushButton('应用')
        self.btn_apply.setFixedSize(60, 30)
        self.btn_apply.setStyleSheet(BTN_STYLE)
        self.btn_apply.setStatusTip('保存并应用修改')
        self.btn_apply.clicked.connect(self.on_btn_apply_clicked)

        layout_bottom = QHBoxLayout()
        layout_bottom.setContentsMargins(0, 0, 20, 0)
        layout_bottom.setSpacing(5)
        layout_bottom.addStretch(1)
        layout_bottom.addWidget(self.btn_defualt)
        layout_bottom.addWidget(self.btn_cancel)
        layout_bottom.addWidget(self.btn_apply)

#-------------------------------------------------------
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.setSpacing(3)
        mainLayout.addWidget(self.sa_Settings)
        mainLayout.addLayout(layout_bottom)

        self.setLayout(mainLayout)

    def resetData(self):
        self.lineedit_SVM.setText(self.config.get('Model', 'SVM'))
        self.lineedit_ANN.setText(self.config.get('Model', 'ANN'))
        self.lineedit_ChineseANN.setText(self.config.get('Model', 'ChineseANN'))
        self.lineedit_GrayChANN.setText(self.config.get('Model', 'GrayChANN'))
        self.lineedit_ChineseMapping.setText(self.config.get('Model', 'ChineseMapping'))

    def defualtData(self):
        self.config.read("resources/config/defualt.ini")
        self.resetData()
        self.config.write(open("resources/config/siripr.ini", "w"))

    def on_btn_SVM_clicked(self):
        path = QFileDialog.getOpenFileName(self, "设置SVM模型路径", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_SVM.setText(path)

    def on_btn_ANN_clicked(self):
        path = QFileDialog.getOpenFileName(self, "设置ANN模型路径", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_ANN.setText(path)

    def on_btn_ChineseANN_clicked(self):
        path = QFileDialog.getOpenFileName(self, "设置ChineseANN模型路径", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_ChineseANN.setText(path)

    def on_btn_GrayChANN_clicked(self):
        path = QFileDialog.getOpenFileName(self, "设置GrayChANN模型路径", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_GrayChANN.setText(path)

    def on_btn_ChineseMapping_clicked(self):
        path = QFileDialog.getOpenFileName(self, "设置ChineseMapping模型路径", "./resources/model",
                                           "File(*)")[0]
        if len(path) != 0:
            self.lineedit_ChineseMapping.setText(path)

    def on_btn_defualt_clicked(self):
        self.defualtData()

    def on_btn_cancel_clicked(self):
        self.resetData()

    def on_btn_apply_clicked(self):
        self.saveConfig()

    def saveConfig(self):
        self.config.set('Model', 'SVM', self.lineedit_SVM.text())
        self.config.set('Model', 'ANN', self.lineedit_ANN.text())
        self.config.set('Model', 'ChineseANN', self.lineedit_ChineseANN.text())
        self.config.set('Model', 'GrayChANN', self.lineedit_GrayChANN.text())
        self.config.set('Model', 'ChineseMapping', self.lineedit_ChineseMapping.text())
        self.config.write(open("resources/config/siripr.ini", "w"))
        self.fWindow.plateRecognize.loadModel()