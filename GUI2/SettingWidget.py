# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:SettingWidget.py
@time:2020/4/5 15:59
"""

import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFileDialog, \
    QPushButton, QScrollArea,QGridLayout,QCheckBox,QSpinBox,QComboBox

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
            background:#FBFAFA;
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
        
        QComboBox{
            font-family:Microsoft YaHei;
            border:1px solid #B5ADAD;
            border-radius:2px;
            background: #fff;
            font:12px;
            color:dimgray;
        }
        QComboBox QAbstractItemView{
            border: 0px;
            outline:0px;
            selection-background-color: #2C2A28;
            height:100px;
            background: #fff;
            font-size:12px
        }
        QComboBox QAbstractItemView::item {
            height:30px;
        }
        QComboBox QAbstractItemView::item:selected{
            background-color: #f1f1f1;
        }
        QComboBox::down-arrow{
            background: #fff;
            color:dimgray;
        }
        QComboBox::drop-down{
            border:0px;
        }
        
        
        QSpinBox{
            border:1px solid #B5ADAD;
            height: 21px;
        }
        /*spinbox 抬起样式*/
        QTimeEdit::up-button,QDoubleSpinBox::up-button,QSpinBox::up-button {subcontrol-origin:border;
            subcontrol-position:right;
            image: url(./GUI2/img/spinbox_up_right.png);
            width: 12px;
            height: 20px;       
        }
        QTimeEdit::down-button,QDoubleSpinBox::down-button,QSpinBox::down-button {subcontrol-origin:border;
            subcontrol-position:left;
            border-image: url(./GUI2/img/spinbox_up_left.png);
            width: 12px;
            height: 20px;
        }
        /*按钮按下样式*/
        QTimeEdit::up-button:pressed,QDoubleSpinBox::up-button:pressed,QSpinBox::up-button:pressed{subcontrol-origin:border;
            subcontrol-position:right;
            image: url(./GUI2/img/spinbox_down_right.png);
            width: 12px;
            height: 20px;       
        }
        QTimeEdit::down-button:pressed,QDoubleSpinBox::down-button:pressed,QSpinBox::down-button:pressed,QSpinBox::down-button:pressed{
            subcontrol-position:left;
            image: url(./GUI2/img/spinbox_down_left.png);
            width: 12px;
            height: 20px;
        }
        
        /*RadioButton和checkbox字体和间距设置*/
        QRadioButton ,QCheckBox{
            spacing: 5px;
            font-size: 12px;
        }
        /*checkbox样式设置*/
        QCheckBox::indicator { 
            width: 26px;
            height: 30px;
        }
        /*未选中*/
        QCheckBox::indicator::unchecked {   
            image: url(./GUI2/img/iosCheckBoxOff.png);
        }
        /*选中*/
        QCheckBox::indicator::checked { 
            image: url(./GUI2/img/iosCheckBoxOn.png);
        }
        """

class SettingWidget(QWidget):

    def __init__(self, fWind):
        super().__init__()
        self.fWindow=fWind

        self.config = configparser.ConfigParser()
        self.config.read("resources/config/siripr.ini")

        self.initUI()
        self.resetData()

    def initUI(self):

        """------------------模型路径设置------------------"""
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

        """------------------图片识别设置------------------"""
        self.label_ImgPR = QLabel('图片识别设置')
        self.label_ImgPR.setFixedHeight(20)
        self.label_ImgPR.setAlignment(Qt.AlignCenter)

        self.label_ImgPR_debug=QLabel('调试:')
        self.label_ImgPR_debug.setFixedSize(40, 30)
        self.label_ImgPR_debug.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.checkbox_ImgPR_debug=QCheckBox()
        self.checkbox_ImgPR_debug.setFixedSize(100, 30)

        layout_ImgPR_debug = QHBoxLayout()
        layout_ImgPR_debug.setContentsMargins(0, 5, 0, 0)
        layout_ImgPR_debug.setSpacing(5)
        layout_ImgPR_debug.addWidget(self.label_ImgPR_debug)
        layout_ImgPR_debug.addWidget(self.checkbox_ImgPR_debug)
        layout_ImgPR_debug.addStretch()

        self.label_ImgPR_label = QLabel('标注结果:')
        self.label_ImgPR_label.setFixedSize(65, 30)
        self.label_ImgPR_label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.checkbox_ImgPR_label = QCheckBox()
        self.checkbox_ImgPR_label.setFixedSize(100, 30)

        layout_ImgPR_label = QHBoxLayout()
        layout_ImgPR_label.setContentsMargins(0, 5, 0, 0)
        layout_ImgPR_label.setSpacing(5)
        layout_ImgPR_label.addWidget(self.label_ImgPR_label)
        layout_ImgPR_label.addWidget(self.checkbox_ImgPR_label)
        layout_ImgPR_label.addStretch()

        self.label_ImgPR_detecttype = QLabel('检测类型:')
        self.label_ImgPR_detecttype.setFixedSize(65, 30)
        self.label_ImgPR_detecttype.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.combobox_ImgPR_detecttype = QComboBox()
        self.combobox_ImgPR_detecttype.setFixedSize(120,20)
        self.combobox_ImgPR_detecttype.addItems(
            ['SOBEL', 'COLOR', 'CMSER', 'SOBEL&COLOR', 'SOBEL&CMSER', 'COLOR&CMSER', 'All'])

        layout_ImgPR_detecttype = QHBoxLayout()
        layout_ImgPR_detecttype.setContentsMargins(0, 5, 0, 0)
        layout_ImgPR_detecttype.setSpacing(5)
        layout_ImgPR_detecttype.addWidget(self.label_ImgPR_detecttype)
        layout_ImgPR_detecttype.addWidget(self.combobox_ImgPR_detecttype)
        layout_ImgPR_detecttype.addStretch()

        self.label_ImgPR_maxplates = QLabel('最大车牌上限:')
        self.label_ImgPR_maxplates.setFixedSize(90, 30)
        self.label_ImgPR_maxplates.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_ImgPR_maxplates = QSpinBox()
        self.spinbox_ImgPR_maxplates.setFixedSize(50, 22)
        self.spinbox_ImgPR_maxplates.setAlignment(Qt.AlignCenter)
        self.spinbox_ImgPR_maxplates.setMinimum(1)
        self.spinbox_ImgPR_maxplates.setMaximum(10)

        layout_ImgPR_maxplates = QHBoxLayout()
        layout_ImgPR_maxplates.setContentsMargins(0, 5, 0, 0)
        layout_ImgPR_maxplates.setSpacing(5)
        layout_ImgPR_maxplates.addWidget(self.label_ImgPR_maxplates)
        layout_ImgPR_maxplates.addWidget(self.spinbox_ImgPR_maxplates)
        layout_ImgPR_maxplates.addStretch()

        self.label_ImgPR_OutPutPath = QLabel('识别结果保存路径:')
        self.label_ImgPR_OutPutPath.setFixedSize(200, 20)
        self.label_ImgPR_OutPutPath.setAlignment(Qt.AlignLeft)
        self.lineedit_ImgPR_OutPutPath = QLineEdit()
        self.lineedit_ImgPR_OutPutPath.setFixedHeight(30)
        self.btn_ImgPR_OutPutPath = QPushButton('...')
        self.btn_ImgPR_OutPutPath.setStyleSheet(BTN_STYLE)
        self.btn_ImgPR_OutPutPath.setFixedSize(30, 30)
        self.btn_ImgPR_OutPutPath.clicked.connect(self.on_btn_ImgPR_OutPutPath_clicked)

        layout_ImgPR_OutPutPath = QGridLayout()
        layout_ImgPR_OutPutPath.setContentsMargins(0, 5, 0, 0)
        layout_ImgPR_OutPutPath.setSpacing(5)
        layout_ImgPR_OutPutPath.addWidget(self.label_ImgPR_OutPutPath, 0, 0)
        layout_ImgPR_OutPutPath.addWidget(self.lineedit_ImgPR_OutPutPath, 1, 0)
        layout_ImgPR_OutPutPath.addWidget(self.btn_ImgPR_OutPutPath, 1, 1)

        layout_ImgPR = QVBoxLayout()
        layout_ImgPR.setContentsMargins(5, 10, 5, 0)
        layout_ImgPR.setSpacing(10)
        layout_ImgPR.addWidget(self.label_ImgPR)
        layout_ImgPR.addLayout(layout_ImgPR_debug)
        layout_ImgPR.addLayout(layout_ImgPR_label)
        layout_ImgPR.addLayout(layout_ImgPR_detecttype)
        layout_ImgPR.addLayout(layout_ImgPR_maxplates)
        layout_ImgPR.addLayout(layout_ImgPR_OutPutPath)

        """------------------视频识别设置------------------"""
        self.label_VideoPR = QLabel('视频识别设置')
        self.label_VideoPR.setFixedHeight(20)
        self.label_VideoPR.setAlignment(Qt.AlignCenter)

        self.label_VideoPR_recognize = QLabel('识别:')
        self.label_VideoPR_recognize.setFixedSize(40, 30)
        self.label_VideoPR_recognize.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.checkbox_VideoPR_recognize = QCheckBox()
        self.checkbox_VideoPR_recognize.setFixedSize(100, 30)

        layout_VideoPR_recognize = QHBoxLayout()
        layout_VideoPR_recognize.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_recognize.setSpacing(5)
        layout_VideoPR_recognize.addWidget(self.label_VideoPR_recognize)
        layout_VideoPR_recognize.addWidget(self.checkbox_VideoPR_recognize)
        layout_VideoPR_recognize.addStretch()

        self.label_VideoPR_record = QLabel('录制:')
        self.label_VideoPR_record.setFixedSize(40, 30)
        self.label_VideoPR_record.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.checkbox_VideoPR_record = QCheckBox()
        self.checkbox_VideoPR_record.setFixedSize(100, 30)

        layout_VideoPR_record = QHBoxLayout()
        layout_VideoPR_record.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_record.setSpacing(5)
        layout_VideoPR_record.addWidget(self.label_VideoPR_record)
        layout_VideoPR_record.addWidget(self.checkbox_VideoPR_record)
        layout_VideoPR_record.addStretch()

        self.label_VideoPR_debug = QLabel('调试:')
        self.label_VideoPR_debug.setFixedSize(40, 30)
        self.label_VideoPR_debug.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.checkbox_VideoPR_debug = QCheckBox()
        self.checkbox_VideoPR_debug.setFixedSize(100, 30)

        layout_VideoPR_debug = QHBoxLayout()
        layout_VideoPR_debug.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_debug.setSpacing(5)
        layout_VideoPR_debug.addWidget(self.label_VideoPR_debug)
        layout_VideoPR_debug.addWidget(self.checkbox_VideoPR_debug)
        layout_VideoPR_debug.addStretch()

        self.label_VideoPR_label = QLabel('标注结果:')
        self.label_VideoPR_label.setFixedSize(65, 30)
        self.label_VideoPR_label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.checkbox_VideoPR_label = QCheckBox()
        self.checkbox_VideoPR_label.setFixedSize(100, 30)

        layout_VideoPR_label = QHBoxLayout()
        layout_VideoPR_label.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_label.setSpacing(5)
        layout_VideoPR_label.addWidget(self.label_VideoPR_label)
        layout_VideoPR_label.addWidget(self.checkbox_VideoPR_label)
        layout_VideoPR_label.addStretch()

        self.label_VideoPR_detecttype = QLabel('检测类型:')
        self.label_VideoPR_detecttype.setFixedSize(65, 30)
        self.label_VideoPR_detecttype.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.combobox_VideoPR_detecttype = QComboBox()
        self.combobox_VideoPR_detecttype.setFixedSize(120, 20)
        self.combobox_VideoPR_detecttype.addItems(
            ['SOBEL', 'COLOR', 'CMSER', 'SOBEL&COLOR', 'SOBEL&CMSER', 'COLOR&CMSER', 'All'])

        layout_VideoPR_detecttype = QHBoxLayout()
        layout_VideoPR_detecttype.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_detecttype.setSpacing(5)
        layout_VideoPR_detecttype.addWidget(self.label_VideoPR_detecttype)
        layout_VideoPR_detecttype.addWidget(self.combobox_VideoPR_detecttype)
        layout_VideoPR_detecttype.addStretch()

        self.label_VideoPR_maxplates = QLabel('最大车牌上限:')
        self.label_VideoPR_maxplates.setFixedSize(90, 30)
        self.label_VideoPR_maxplates.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_VideoPR_maxplates = QSpinBox()
        self.spinbox_VideoPR_maxplates.setFixedSize(50, 22)
        self.spinbox_VideoPR_maxplates.setAlignment(Qt.AlignCenter)
        self.spinbox_VideoPR_maxplates.setMinimum(1)
        self.spinbox_VideoPR_maxplates.setMaximum(10)

        layout_VideoPR_maxplates = QHBoxLayout()
        layout_VideoPR_maxplates.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_maxplates.setSpacing(5)
        layout_VideoPR_maxplates.addWidget(self.label_VideoPR_maxplates)
        layout_VideoPR_maxplates.addWidget(self.spinbox_VideoPR_maxplates)
        layout_VideoPR_maxplates.addStretch()

        self.label_VideoPR_OutPutPath = QLabel('识别结果保存路径:')
        self.label_VideoPR_OutPutPath.setFixedSize(200, 20)
        self.label_VideoPR_OutPutPath.setAlignment(Qt.AlignLeft)
        self.lineedit_VideoPR_OutPutPath = QLineEdit()
        self.lineedit_VideoPR_OutPutPath.setFixedHeight(30)
        self.btn_VideoPR_OutPutPath = QPushButton('...')
        self.btn_VideoPR_OutPutPath.setStyleSheet(BTN_STYLE)
        self.btn_VideoPR_OutPutPath.setFixedSize(30, 30)
        self.btn_VideoPR_OutPutPath.clicked.connect(self.on_btn_VideoPR_OutPutPath_clicked)

        layout_VideoPR_OutPutPath = QGridLayout()
        layout_VideoPR_OutPutPath.setContentsMargins(0, 5, 0, 0)
        layout_VideoPR_OutPutPath.setSpacing(5)
        layout_VideoPR_OutPutPath.addWidget(self.label_VideoPR_OutPutPath, 0, 0)
        layout_VideoPR_OutPutPath.addWidget(self.lineedit_VideoPR_OutPutPath, 1, 0)
        layout_VideoPR_OutPutPath.addWidget(self.btn_VideoPR_OutPutPath, 1, 1)

        layout_VideoPR = QVBoxLayout()
        layout_VideoPR.setContentsMargins(5, 10, 5, 0)
        layout_VideoPR.setSpacing(10)
        layout_VideoPR.addWidget(self.label_VideoPR)
        layout_VideoPR.addLayout(layout_VideoPR_recognize)
        layout_VideoPR.addLayout(layout_VideoPR_record)
        layout_VideoPR.addLayout(layout_VideoPR_debug)
        layout_VideoPR.addLayout(layout_VideoPR_label)
        layout_VideoPR.addLayout(layout_VideoPR_detecttype)
        layout_VideoPR.addLayout(layout_VideoPR_maxplates)
        layout_VideoPR.addLayout(layout_VideoPR_OutPutPath)



        """------------------QScrollArea------------------"""
        sa_contentLayout = QVBoxLayout()
        sa_contentLayout.setContentsMargins(0, 0, 0, 0)
        sa_contentLayout.setSpacing(10)
        sa_contentLayout.addLayout(layout_ModelPath)
        sa_contentLayout.addLayout(layout_ImgPR)
        sa_contentLayout.addLayout(layout_VideoPR)
        sa_contentLayout.addStretch()

        self.sa_contentWidget = QWidget()
        self.sa_contentWidget.setFixedSize(600, 1100)
        self.sa_contentWidget.setLayout(sa_contentLayout)

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

        if self.config.get('IMGPR','debug')=='True':
            self.checkbox_ImgPR_debug.setCheckState(Qt.Checked)
        else:
            self.checkbox_ImgPR_debug.setCheckState(Qt.Unchecked)
        if self.config.get('IMGPR','label')=='True':
            self.checkbox_ImgPR_label.setCheckState(Qt.Checked)
        else:
            self.checkbox_ImgPR_label.setCheckState(Qt.Unchecked)
        self.combobox_ImgPR_detecttype.setCurrentIndex(int(self.config.get('IMGPR','detecttype')))
        self.spinbox_ImgPR_maxplates.setValue(int(self.config.get('IMGPR','maxplates')))
        self.lineedit_ImgPR_OutPutPath.setText(self.config.get('IMGPR','outputpath'))

        if self.config.get('VIDEOPR','recognize')=='True':
            self.checkbox_VideoPR_recognize.setCheckState(Qt.Checked)
        else:
            self.checkbox_VideoPR_recognize.setCheckState(Qt.Unchecked)
        if self.config.get('VIDEOPR','record')=='True':
            self.checkbox_VideoPR_record.setCheckState(Qt.Checked)
        else:
            self.checkbox_VideoPR_record.setCheckState(Qt.Unchecked)
        if self.config.get('VIDEOPR','debug')=='True':
            self.checkbox_VideoPR_debug.setCheckState(Qt.Checked)
        else:
            self.checkbox_VideoPR_debug.setCheckState(Qt.Unchecked)
        if self.config.get('VIDEOPR','label')=='True':
            self.checkbox_VideoPR_label.setCheckState(Qt.Checked)
        else:
            self.checkbox_VideoPR_label.setCheckState(Qt.Unchecked)
        self.combobox_VideoPR_detecttype.setCurrentIndex(int(self.config.get('VIDEOPR','detecttype')))
        self.spinbox_VideoPR_maxplates.setValue(int(self.config.get('VIDEOPR','maxplates')))
        self.lineedit_VideoPR_OutPutPath.setText(self.config.get('VIDEOPR', 'outputpath'))

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

    def on_btn_ImgPR_OutPutPath_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "设置图片识别结果保存路径", "./resources/image/result")
        if len(path) != 0:
            self.lineedit_ImgPR_OutPutPath.setText(path)

    def on_btn_VideoPR_OutPutPath_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "设置图片识别结果保存路径", "./resources/video/result")
        if len(path) != 0:
            self.lineedit_VidoePR_OutPutPath.setText(path)

    def on_btn_defualt_clicked(self):
        self.defualtData()

    def on_btn_cancel_clicked(self):
        self.resetData()

    def on_btn_apply_clicked(self):
        self.saveConfig()

    def show(self):
        self.resetData()
        super().show()

    def saveConfig(self):
        self.config.set('Model', 'SVM', self.lineedit_SVM.text())
        self.config.set('Model', 'ANN', self.lineedit_ANN.text())
        self.config.set('Model', 'ChineseANN', self.lineedit_ChineseANN.text())
        self.config.set('Model', 'GrayChANN', self.lineedit_GrayChANN.text())
        self.config.set('Model', 'ChineseMapping', self.lineedit_ChineseMapping.text())

        if self.checkbox_ImgPR_debug.isChecked():
            self.config.set('IMGPR', 'debug',"True")
        else:
            self.config.set('IMGPR', 'debug', "False")
        if self.checkbox_ImgPR_label.isChecked():
            self.config.set('IMGPR', 'label',"True")
        else:
            self.config.set('IMGPR', 'label', "False")
        self.config.set('IMGPR', 'detecttype', str(self.combobox_ImgPR_detecttype.currentIndex()))
        self.config.set('IMGPR', 'maxplates', str(self.spinbox_ImgPR_maxplates.value()))
        self.config.set('IMGPR', 'outputpath',self.lineedit_ImgPR_OutPutPath.text())

        if self.checkbox_VideoPR_recognize.isChecked():
            self.config.set('VIDEOPR', 'recognize',"True")
        else:
            self.config.set('VIDEOPR', 'recognize', "False")
        if self.checkbox_VideoPR_record.isChecked():
            self.config.set('VIDEOPR', 'record',"True")
        else:
            self.config.set('VIDEOPR', 'record', "False")
        if self.checkbox_VideoPR_debug.isChecked():
            self.config.set('VIDEOPR', 'debug',"True")
        else:
            self.config.set('VIDEOPR', 'debug', "False")
        if self.checkbox_VideoPR_label.isChecked():
            self.config.set('VIDEOPR', 'label',"True")
        else:
            self.config.set('VIDEOPR', 'label', "False")
        self.config.set('VIDEOPR', 'detecttype', str(self.combobox_VideoPR_detecttype.currentIndex()))
        self.config.set('VIDEOPR', 'maxplates', str(self.spinbox_VideoPR_maxplates.value()))
        self.config.set('VIDEOPR', 'outputpath', self.lineedit_VideoPR_OutPutPath.text())

        self.config.write(open("resources/config/siripr.ini", "w"))
        self.fWindow.plateRecognize.loadModel()