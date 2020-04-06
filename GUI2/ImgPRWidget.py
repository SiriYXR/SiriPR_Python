# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:ImgPRWidget.py
@time:2020/4/5 15:58
"""

from time import time
import os

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QCheckBox, QHBoxLayout, QScrollArea, \
    QSpinBox

from prmod.core.CPlate import CPlate
from prmod.util.Utiles import *

MAIN_STYLE="""
    
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
        """

IOS_CHECKBOX_STYLE="""
        /*RadioButton和checkbox字体和间距设置*/
        QRadioButton ,QCheckBox{
            spacing: 5px;
            font-size: 12px;
        }
        /*checkbox样式设置*/
        QCheckBox::indicator { 
            width: 26px;
            height: 50px;
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

class ImgPRWidget(QWidget):

    def __init__(self, fwind):
        super().__init__()

        self.fWindow = fwind

        self.cvimg = None
        self.qimg = None
        self.plate = None
        self.filelist = []
        self.platelist = None
        self.fileindex = -1
        self.plateindex = -1

        self.initUI()

    def initData(self):
        self.cvimg = None
        self.qimg = None
        self.plate = None
        self.filelist = []
        self.platelist = None
        self.fileindex = -1
        self.plateindex = -1

    def initUI(self):
        self.setStyleSheet(MAIN_STYLE)

        self.selectAllImgCheckBox = QCheckBox("全选")

        self.inportBtn = QPushButton("+")
        self.inportBtn.setFixedSize(25,25)
        self.inportBtn.setStatusTip('导入图片文件')
        self.inportBtn.clicked.connect(self.on_btn_inport_clicked)

        self.removeBtn = QPushButton("-")
        self.removeBtn.setFixedSize(25, 25)
        self.removeBtn.setStatusTip('移除图片文件')

        self.outportBtn = QPushButton("导出")
        self.outportBtn.setFixedSize(40, 25)
        self.outportBtn.setStatusTip('导出图片识别结果')

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(0)
        topLayout.addWidget(self.selectAllImgCheckBox)
        topLayout.addWidget(self.inportBtn)
        topLayout.addWidget(self.removeBtn)
        topLayout.addWidget(self.outportBtn)

        self.imgListScrollArea = QScrollArea()
        self.imgListScrollArea.setFixedWidth(200)

        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        bottomLayout.setSpacing(0)
        bottomLayout.addWidget(self.imgListScrollArea)

        """--------------------sourceLayout------------------------"""

        sourceLayout = QVBoxLayout()
        sourceLayout.setContentsMargins(5, 0, 0, 0)
        sourceLayout.setSpacing(0)
        sourceLayout.addLayout(topLayout)
        sourceLayout.addLayout(bottomLayout)

        """-------------------- topLayout------------------------"""

        self.label_RunningMSG = QLabel()
        self.label_RunningMSG.setAlignment(Qt.AlignCenter)
        self.label_RunningMSG.setFixedHeight(25)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.label_RunningMSG)

        """--------------------------------------------"""
        self.imgLabel = QLabel("导入一张图片 ")
        self.imgLabel.setAlignment(Qt.AlignCenter)

        sa_img = QScrollArea()
        sa_img.setWidget(self.imgLabel)
        sa_img.setAlignment(Qt.AlignCenter)

        """-------------------- imgListlayout------------------------"""
        self.currentFilePathLabel = QLabel()
        self.currentFilePathLabel.setFixedHeight(30)

        self.btn_last_img = QPushButton("<")
        self.btn_last_img.setFixedSize(30, 30)
        self.btn_last_img.setStatusTip('加载上一张图片')
        self.btn_last_img.clicked.connect(self.on_btn_last_img_clicked)

        self.btn_next_img = QPushButton(">")
        self.btn_next_img.setFixedSize(30, 30)
        self.btn_next_img.setStatusTip('加载下一张图片')
        self.btn_next_img.clicked.connect(self.on_btn_next_img_clicked)

        imgListlayout = QHBoxLayout()
        imgListlayout.setContentsMargins(0, 2, 0, 0)
        imgListlayout.setSpacing(5)
        imgListlayout.addWidget(self.btn_last_img)
        imgListlayout.addWidget(self.currentFilePathLabel)
        imgListlayout.addWidget(self.btn_next_img)

        """--------------------prOPlayout------------------------"""
        self.btn_recognize = QPushButton("识别")
        self.btn_recognize.setFixedSize(100, 30)
        self.btn_recognize.setStatusTip('识别当前图片')
        self.btn_recognize.clicked.connect(self.on_btn_recognize_clicked)

        self.resLabel = QLabel("")
        self.resLabel.setAlignment(Qt.AlignCenter)
        self.resLabel.setFixedHeight(30)

        self.combobox_Plate = MyComboBox()
        self.combobox_Plate.setFixedHeight(30)
        self.combobox_Plate.popupAboutToBeShown.connect(self.on_combobox_Plate_clicked)

        self.btn_last_plate = QPushButton("<")
        self.btn_last_plate.setFixedSize(30, 30)
        self.btn_last_plate.setStatusTip('上一张车牌')
        self.btn_last_plate.clicked.connect(self.on_btn_last_plate_clicked)

        self.btn_next_plate = QPushButton(">")
        self.btn_next_plate.setFixedSize(30, 30)
        self.btn_next_plate.setStatusTip('下一张车牌')
        self.btn_next_plate.clicked.connect(self.on_btn_next_plate_clicked)

        prOPlayout = QHBoxLayout()
        prOPlayout.setContentsMargins(0, 2, 0, 0)
        prOPlayout.setSpacing(5)
        prOPlayout.addWidget(self.btn_recognize)
        prOPlayout.addWidget(self.btn_last_plate)
        prOPlayout.addWidget(self.combobox_Plate)
        prOPlayout.addWidget(self.btn_next_plate)

        """--------------------setinglayout------------------------"""
        self.cb_debug = QCheckBox("调试")
        self.cb_debug.setStyleSheet(IOS_CHECKBOX_STYLE)
        self.cb_label = QCheckBox("标注结果")
        self.cb_label.setStyleSheet(IOS_CHECKBOX_STYLE)

        self.label_DetectType = QLabel(' 检测类型')
        self.combobox_DetectType = QComboBox()
        self.combobox_DetectType.addItems(
            ['SOBEL', 'COLOR', 'CMSER', 'SOBEL&COLOR', 'SOBEL&CMSER', 'COLOR&CMSER', 'All'])
        self.combobox_DetectType.setStatusTip('设置检测类型')

        self.label_MaxPlates = QLabel(' 最大车牌上限')
        self.spinbox_MaxPlates = QSpinBox()
        self.spinbox_MaxPlates.setFixedSize(50,22)
        self.spinbox_MaxPlates.setAlignment(Qt.AlignCenter)
        self.spinbox_MaxPlates.setMinimum(1)
        self.spinbox_MaxPlates.setMaximum(10)
        self.spinbox_MaxPlates.setStatusTip('设置单张图片检测车牌最大数量')

        settingLayout = QHBoxLayout()
        settingLayout.setContentsMargins(5, 5, 5, 0)
        settingLayout.setSpacing(5)
        settingLayout.addWidget(self.cb_debug)
        settingLayout.addWidget(self.cb_label)
        settingLayout.addWidget(self.label_DetectType)
        settingLayout.addWidget(self.combobox_DetectType)
        settingLayout.addWidget(self.label_MaxPlates)
        settingLayout.addWidget(self.spinbox_MaxPlates)
        settingLayout.addStretch(1)

        """--------------------recognizeLayout------------------------"""
        recognizeLayout = QVBoxLayout()
        recognizeLayout.setContentsMargins(5,0,5,0)
        recognizeLayout.setSpacing(0)
        recognizeLayout.addLayout(topLayout)
        recognizeLayout.addWidget(sa_img)
        recognizeLayout.addLayout(imgListlayout)
        recognizeLayout.addLayout(prOPlayout)
        recognizeLayout.addLayout(settingLayout)


        """--------------------mainLayout------------------------"""
        mainLayout=QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        mainLayout.addLayout(sourceLayout)
        mainLayout.addLayout(recognizeLayout)

        self.setLayout(mainLayout)


    @pyqtSlot(bool)
    def on_btn_last_img_clicked(self, checked):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return
        if self.fileindex == 0:
            self.fWindow.statusBar().showMessage('这是第一张图片!')
            return

        self.fileindex -= 1
        self.currentFilePathLabel.setText(self.filelist[self.fileindex]['path'])

    @pyqtSlot(bool)
    def on_btn_next_img_clicked(self, checked):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return
        if self.fileindex == len(self.filelist) - 1:
            self.fWindow.statusBar().showMessage('这是最后一张图片!')
            return

        self.fileindex += 1


    @pyqtSlot(bool)
    def on_btn_inport_clicked(self, checked):
        pathlist = QFileDialog.getOpenFileNames(self, "打开文件", "./resources/image",
                                                     "图片文件(*.jpg *.jpeg *.png)")[0]

        for i in pathlist:
            self.filelist.append({
                'path':i,
                'name':os.path.basename(i),
                'ticked':True,
                'plates':[],
            })

        if len(self.filelist)>0:
            self.combobox_File.clear()
            for i in range(len(self.filelist)):
               pass
            self.fileindex = 0
            self.openIMG(self.filelist[self.fileindex])

    @pyqtSlot(bool)
    def on_btn_recognize_clicked(self, checked):

        if self.qimg != None:
            self.plate = CPlate()
            self.label_RunningMSG.setText('图片识别中...')

            self.fWindow.plateRecognize.setDebug(self.cb_debug.isChecked())
            self.fWindow.plateRecognize.setDetectType(self.combobox_DetectType.currentIndex())
            self.fWindow.plateRecognize.setMaxPlates(self.spinbox_MaxPlates.value())

            begin = time()
            self.platelist = self.fWindow.plateRecognize.plateRecognize(numpy.copy(self.cvimg))
            end = time()
            runtime = end - begin

            platenum = len(self.platelist)

            if platenum != 0:
                self.filelist[self.fileindex]['plates']=self.platelist
                self.plateindex = 0
                self.combobox_Plate.clear()
                for i in range(platenum):
                    self.plate.license, self.plate.x, self.plate.y, self.plate.w, self.plate.h = self.platelist[i]
                    self.combobox_Plate.insertItem(i, "{p.license} {p.x} {p.y} {p.w} {p.h}".format(p=self.plate))

                self.label_RunningMSG.setText(
                    '图片识别完成！     发现 {plates} 张车牌    运行时间:{runtime:.3f}s'.format(
                        plates=platenum, runtime=runtime))

                self.setShowPlate()
            else:
                self.label_RunningMSG.setText('没有发现车牌!')
        else:
            self.fWindow.statusBar().showMessage('请先导入图片!')

    def on_combobox_Plate_clicked(self):
        if self.plateindex == -1:
            return
        self.plateindex = self.combobox_Plate.currentIndex()
        self.setShowPlate()

    @pyqtSlot(bool)
    def on_btn_next_plate_clicked(self, checked):
        if self.plateindex == -1:
            self.fWindow.statusBar().showMessage('没有车牌!')
            return

        if self.plateindex == len(self.platelist) - 1:
            self.fWindow.statusBar().showMessage('这是最后一块车牌!')
            return

        self.plateindex += 1
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.on_combobox_Plate_clicked()

    @pyqtSlot(bool)
    def on_btn_last_plate_clicked(self, checked):
        if self.plateindex == -1:
            self.fWindow.statusBar().showMessage('没有车牌!')
            return

        if self.plateindex == 0:
            self.fWindow.statusBar().showMessage('这是第一张车牌!')
            return

        self.plateindex -= 1
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.on_combobox_Plate_clicked()

    def initButton(self):
        self.label_RunningMSG.clear()
        self.imgLabel.clear()
        self.imgLabel.setText('导入图片文件')
        self.combobox_Plate.clear()
        self.combobox_DetectType.setCurrentIndex(0)
        self.spinbox_MaxPlates.setValue(1)
        self.cb_debug.setCheckState(False)
        self.cb_label.setCheckState(False)

    def show(self):
        self.initButton()
        self.initData()
        super().show()

    def openIMG(self, filename):
        self.cvimg = cv_imread(filename, 1)
        self.qimg = CV2QImage(numpy.copy(self.cvimg))
        if (self.qimg != None):
            self.fWindow.statusBar().showMessage('图片打开成功！')
        else:
            self.fWindow.statusBar().showMessage('图片打开失败！')

    def setShowIMG(self, cv_img):
        qimg = CV2QImage(numpy.copy(cv_img))
        self.imgLabel.setPixmap(QPixmap.fromImage(qimg))
        self.imgLabel.resize(qimg.size().width(), qimg.size().height())

    def setShowPlate(self):
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.plate.license, self.plate.x, self.plate.y, self.plate.w, self.plate.h = self.platelist[self.plateindex]

        if self.cb_label.isChecked():
            temp = numpy.copy(self.cvimg)
            temp = cv2.rectangle(temp, (self.plate.x, self.plate.y),
                                 (self.plate.x + self.plate.w, self.plate.y + self.plate.h), (0, 255, 0), 2)
            self.setShowIMG(temp)
        else:
            self.imgLabel.setPixmap(QPixmap.fromImage(self.qimg))
            self.imgLabel.resize(self.qimg.width(), self.qimg.height())

    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Escape:
            self.fWindow.on_indexAct_clicked()
            return

        super().keyPressEvent(event)
