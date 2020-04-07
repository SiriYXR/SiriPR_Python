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
from PyQt5.QtWidgets import QWidget,  QPushButton, QVBoxLayout, QFileDialog, QCheckBox, QHBoxLayout, QScrollArea, \
    QSpinBox

from GUI2.ImgFileWidget import ImgFileWidget

from prmod.core.CPlate import CPlate
from prmod.util.Utiles import *

MAIN_STYLE="""
        *{
            font-family:Microsoft Yahei;
            font-size:12px;
            color:dimgray;
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
            border:1px solid #B5ADAD;
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
        
        QScrollBar:horizontal
        {
            border-radius:7px;  
            background:#f1f1f1; 
            padding-left:14px;  
            padding-right:14px;  
        }
        QScrollBar::handle:horizontal
        {
            background:#C4CAD0; 
            border-radius:6px;  
            margin-top:2px;  
            margin-bottom:2px;  
        }
        QScrollBar::handle:horizontal:hover
        {
            background:gray;
            border-radius:6px;
        }
        QScrollBar::add-line:horizontal
        {
            height:14px;width:8px;  
            image:url('');  
        }
        QScrollBar::sub-line:horizontal
        {
            height:14px;width:8px;
            image:url('');  
        }
        QScrollBar::add-line:horizontal:hover
        {
            height:14px;width:8px;
            image:url('');
            subcontrol-position:right;
        }
        QScrollBar::sub-line:horizontal:hover
        {
            height:14px;width:8px;
            image:url('');  
            subcontrol-position:left;
        }
        QScrollBar::add-page:horizontal
        {
            background:#f1f1f1;
        }
        QScrollBar::sub-page:horizontal
        {
            background:#f1f1f1; 
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
        self.fileset=set()
        self.checkedlist=[]
        self.fileindex = -1
        self.plateindex = -1

        self.isCheckedAll=True

        self.initUI()

    def initUI(self):
        self.setStyleSheet(MAIN_STYLE)

        self.selectAllImgCheckBox = QCheckBox("全选 (0/0)")
        self.selectAllImgCheckBox.setTristate(False) # 取消半选中状态
        self.selectAllImgCheckBox.setEnabled(False)
        self.selectAllImgCheckBox.clicked.connect(self.selectAllImgCheckBoxClicked)

        self.inportBtn = QPushButton("+")
        self.inportBtn.setFixedSize(25,25)
        self.inportBtn.setStatusTip('导入图片文件')
        self.inportBtn.clicked.connect(self.on_btn_inport_clicked)

        self.removeBtn = QPushButton("-")
        self.removeBtn.setFixedSize(25, 25)
        self.removeBtn.setStatusTip('移除图片文件')
        self.removeBtn.clicked.connect(self.on_btn_remove_clicked)

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

        self.imgListContentLayout=QVBoxLayout()
        self.imgListContentLayout.setContentsMargins(0, 0, 0, 0)
        self.imgListContentLayout.setSpacing(2)

        self.imgListScrollContent=QWidget()
        self.imgListScrollContent.setFixedWidth(190)
        self.imgListScrollContent.setStyleSheet('background-color:#f1f1f1')
        self.imgListScrollContent.setContentsMargins(0, 0, 0, 0)
        self.imgListScrollContent.setLayout(self.imgListContentLayout)

        self.imgListScrollArea = QScrollArea()
        self.imgListScrollArea.setContentsMargins(0,0,0,0)
        self.imgListScrollArea.setStyleSheet(SCROLLAREA_STYLE)
        self.imgListScrollArea.setFixedWidth(200)
        self.imgListScrollArea.setWidget(self.imgListScrollContent)

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
        self.imgLabel = QLabel("导入图片 ")
        self.imgLabel.setAlignment(Qt.AlignCenter)

        self.sa_img = QScrollArea()
        self.sa_img.setStyleSheet(SCROLLAREA_STYLE)
        self.sa_img.setWidget(self.imgLabel)
        self.sa_img.setAlignment(Qt.AlignCenter)

        """-------------------- currentFilePathLayout------------------------"""
        self.currentFilePathLabel = QLabel()
        self.currentFilePathLabel.setAlignment(Qt.AlignCenter)
        self.currentFilePathLabel.setFixedHeight(30)

        self.btn_last_img = QPushButton("<")
        self.btn_last_img.setFixedSize(30, 30)
        self.btn_last_img.setStatusTip('加载上一张图片')
        self.btn_last_img.clicked.connect(self.on_btn_last_img_clicked)

        self.btn_next_img = QPushButton(">")
        self.btn_next_img.setFixedSize(30, 30)
        self.btn_next_img.setStatusTip('加载下一张图片')
        self.btn_next_img.clicked.connect(self.on_btn_next_img_clicked)

        currentFilePathLayout = QHBoxLayout()
        currentFilePathLayout.setContentsMargins(0, 2, 0, 0)
        currentFilePathLayout.setSpacing(5)
        currentFilePathLayout.addWidget(self.btn_last_img)
        currentFilePathLayout.addWidget(self.currentFilePathLabel)
        currentFilePathLayout.addWidget(self.btn_next_img)

        """--------------------prOPlayout------------------------"""
        self.btn_recognize = QPushButton("识别")
        self.btn_recognize.setFixedSize(100, 30)
        self.btn_recognize.setStatusTip('识别当前图片')
        self.btn_recognize.clicked.connect(self.on_btn_recognize_clicked)

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
        recognizeLayout.addWidget(self.sa_img)
        recognizeLayout.addLayout(currentFilePathLayout)
        recognizeLayout.addLayout(prOPlayout)
        recognizeLayout.addLayout(settingLayout)


        """--------------------mainLayout------------------------"""
        mainLayout=QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        mainLayout.addLayout(sourceLayout)
        mainLayout.addLayout(recognizeLayout)

        self.setLayout(mainLayout)



    def on_btn_last_img_clicked(self):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return
        if self.fileindex == 0:
            self.fWindow.statusBar().showMessage('这是第一张图片!')
            return

        self.fileindex -= 1
        self.showImageFile(self.filelist[self.fileindex].file_path)

    def on_btn_next_img_clicked(self):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return
        if self.fileindex == len(self.filelist) - 1:
            self.fWindow.statusBar().showMessage('这是最后一张图片!')
            return

        self.fileindex += 1
        self.showImageFile(self.filelist[self.fileindex].file_path)

    def on_btn_inport_clicked(self):
        pathlist = QFileDialog.getOpenFileNames(self, "打开文件", "./resources/image",
                                                     "图片文件(*.jpg *.jpeg *.png)")[0]
        redundant=0
        for i in pathlist:
            if i in self.fileset :
                redundant+=1
                continue
            self.fileset.add(i)
            w=ImgFileWidget(self,i)
            self.filelist.append(w)
            self.imgListContentLayout.addWidget(w)
        self.imgListScrollContent.setFixedSize(196,len(self.filelist)*27)
        self.fWindow.statusBar().showMessage('成功添加{}张图片，去除冗余图片{}张。'.format(len(pathlist)-redundant,redundant))
        self.selectAllImgCheckBox.setEnabled(True)
        self.updateCheckedList()

    def on_btn_remove_clicked(self):
        tmplist=[]
        currentImgPath=self.filelist[self.fileindex].file_path
        for i in range(len(self.filelist)):
            if i in self.checkedlist:
                self.imgListContentLayout.removeWidget(self.filelist[i])
                self.fileset.remove(self.filelist[i].file_path)
            else:
                tmplist.append(self.filelist[i])
        self.filelist=tmplist

        if self.fileindex in self.checkedlist:
            if len(self.filelist)==0:
                self.fileindex=-1
            else:
                self.fileindex=0
        else:
            for i in range(len(self.filelist)):
                if self.filelist[i].file_path==currentImgPath:
                    self.fileindex=i
                    break

        self.imgListScrollContent.setFixedHeight(len(self.filelist) * 27)
        self.fWindow.statusBar().showMessage('成功移除{}张图片。'.format(len(self.checkedlist)))
        self.updateCheckedList()


    def on_btn_recognize_clicked(self):

        if self.qimg != None:
            self.plate = CPlate()
            self.label_RunningMSG.setText('图片识别中...')

            self.fWindow.plateRecognize.setDebug(self.cb_debug.isChecked())
            self.fWindow.plateRecognize.setDetectType(self.combobox_DetectType.currentIndex())
            self.fWindow.plateRecognize.setMaxPlates(self.spinbox_MaxPlates.value())

            begin = time()
            self.filelist[self.fileindex].plates = self.fWindow.plateRecognize.plateRecognize(numpy.copy(self.cvimg))
            end = time()
            runtime = end - begin

            platenum=len(self.filelist[self.fileindex].plates)
            if platenum != 0:
                self.plateindex = 0
                self.combobox_Plate.clear()
                for i in range(len(self.filelist[self.fileindex].plates)):
                    plate_license, plate_x, plate_y, plate_w, plate_h = self.filelist[self.fileindex].plates[i]
                    self.combobox_Plate.insertItem(i, "{} {} {} {} {}".format(plate_license, plate_x, plate_y, plate_w,
                                                                              plate_h))

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

    def on_btn_next_plate_clicked(self):
        if self.plateindex == -1:
            self.fWindow.statusBar().showMessage('没有车牌!')
            return

        if self.plateindex == len(self.filelist[self.fileindex].plates) - 1:
            self.fWindow.statusBar().showMessage('这是最后一块车牌!')
            return

        self.plateindex += 1
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.on_combobox_Plate_clicked()

    def on_btn_last_plate_clicked(self):
        if self.plateindex == -1:
            self.fWindow.statusBar().showMessage('没有车牌!')
            return

        if self.plateindex == 0:
            self.fWindow.statusBar().showMessage('这是第一张车牌!')
            return

        self.plateindex -= 1
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.on_combobox_Plate_clicked()

    def initPRWidget(self):
        self.label_RunningMSG.clear()
        self.imgLabel.clear()
        self.imgLabel.setText('导入图片')
        self.imgLabel.resize(200,200)
        self.currentFilePathLabel.setText("")
        self.combobox_Plate.clear()
        self.combobox_DetectType.setCurrentIndex(0)
        self.spinbox_MaxPlates.setValue(1)
        self.cb_debug.setCheckState(False)
        self.cb_label.setCheckState(False)
        self.plateindex=-1

    def show(self):
        if self.fileindex==-1:
            self.initPRWidget()
        super().show()

    def showImageFile(self,file_path):
        if self.currentFilePathLabel.text() == file_path:
            self.fWindow.statusBar().showMessage('文件已打开!')
            return
        self.label_RunningMSG.clear()
        self.openIMG(file_path)
        self.setShowQIMG()
        self.currentFilePathLabel.setText(file_path)
        self.upfateFileIndex()
        self.combobox_DetectType.setCurrentIndex(self.filelist[self.fileindex].detecttype_value)
        self.spinbox_MaxPlates.setValue(self.filelist[self.fileindex].maxplates_value)
        self.cb_debug.setCheckState(self.filelist[self.fileindex].debug_value)
        self.cb_label.setCheckState(self.filelist[self.fileindex].label_value)
        self.combobox_Plate.clear()
        for i in range(len(self.filelist[self.fileindex].plates)):
            plate_license, plate_x, plate_y, plate_w, plate_h = self.filelist[self.fileindex].plates[i]
            self.combobox_Plate.insertItem(i, "{} {} {} {} {}".format(plate_license, plate_x, plate_y, plate_w,
                                                                      plate_h))
        if len(self.filelist[self.fileindex].plates)>0:
            self.plateindex = 0
        else:
            self.plateindex = -1

    def openIMG(self, file_path):
        self.cvimg = cv_imread(file_path, 1)
        self.qimg = CV2QImage(numpy.copy(self.cvimg))
        if (self.qimg != None):
            self.fWindow.statusBar().showMessage('图片打开成功！')
        else:
            self.fWindow.statusBar().showMessage('图片打开失败！')

    def setShowPIMG(self, cv_img):
        img = CV2QImage(numpy.copy(cv_img))
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.resize(img.size().width(), img.size().height())

    def setShowQIMG(self):
        self.imgLabel.setPixmap(QPixmap.fromImage(self.qimg))
        self.imgLabel.resize(self.qimg.size().width(), self.qimg.size().height())

    def setShowPlate(self):
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        plate_license, plate_x, plate_y, plate_w, plate_h = self.filelist[self.fileindex].plates[self.plateindex]
        if self.cb_label.isChecked():
            temp = numpy.copy(self.cvimg)
            temp = cv2.rectangle(temp, (plate_x, plate_y),
                                 (plate_x + plate_w, plate_y + plate_h), (0, 255, 0), 2)
            self.setShowPIMG(temp)
        else:
            self.setShowQIMG()

    def keyPressEvent(self, event):

        key = event.key()

        super().keyPressEvent(event)

    def updateCheckedList(self):
        self.checkedlist.clear()
        for i in range(len(self.filelist)):
            if(self.filelist[i].checkBox.isChecked()):
                self.checkedlist.append(i)

        if len(self.checkedlist) == len(self.filelist) and len(self.filelist)!=0:
            self.selectAllImgCheckBox.setCheckState(Qt.Checked)
        else:
            self.selectAllImgCheckBox.setCheckState(Qt.Unchecked)

        self.upfateFileIndex()

        self.selectAllImgCheckBox.setText("全选 ({}/{})".format(len(self.checkedlist),len(self.filelist)))

    def upfateFileIndex(self):
        if len(self.filelist)==0:
            self.initPRWidget()
            self.fileindex=-1
            self.selectAllImgCheckBox.setEnabled(False)
        else:
            self.selectAllImgCheckBox.setEnabled(True)

            if not self.currentFilePathLabel.text() in self.fileset:
                self.fileindex = -1
                self.initPRWidget()
            else:
                for i in range(len(self.filelist)):
                    if self.filelist[i].file_path==self.currentFilePathLabel.text():
                        self.fileindex=i
                        break

    def selectAllImgCheckBoxClicked(self):

        if self.selectAllImgCheckBox.isChecked():
            for i in range(len(self.filelist)):
                self.filelist[i].checkBox.setCheckState(Qt.Checked)
        else:
            for i in range(len(self.filelist)):
                self.filelist[i].checkBox.setCheckState(Qt.Unchecked)
        self.updateCheckedList()