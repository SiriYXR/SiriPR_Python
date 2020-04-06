# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:VideoPRWidget.py
@time:2020/4/5 15:59
"""

from time import time

import cv2
import numpy

from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QAction, QFileDialog, \
    QInputDialog, QSlider, QCheckBox, QSpinBox

from prmod.config import PlayState, VideoType
from prmod.util.Utiles import CV2QImage, VideoPRLabel

MAIN_STYL = """

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
        
        /* 整个拖动条的设置 */
        QSlider::groove{
            border: 1px solid #B5ADAD; /* 边框颜色 */
            height:15px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fff, stop:1 #fff);
            margin: 0px 0; /* 0px 设置已划过的地方高度, "0" 距离父控件的距离*/
        }
        /* 顶部拖动设计 */
        QSlider::handle{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 1px solid #B5ADAD; /*边框*/
            width: 15px;
            
            margin: -5px 0; /*滑块大小设置*/
            border-radius: 0px; /* 圆角设置 */
            background-color: #f1f1f1;
        }
        /* 未滑动的区域 */
        QSlider::add-page:horizontal
        {
            border-radius: 3px;
            
        }
        /* 已划过的设置*/
        QSlider::sub-page:horizontal
        {
            border: 1px solid #B5ADAD; /* 边框颜色 */
            background:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #97D2FB, stop:1 #97D2FB); /* 颜色渐变*/
            border-radius: 3px;
            
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

BTN_STYL="""
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
            background-color:#f1f1f1;
        }
        QPushButton:pressed
        {
            background-color:#f1f1f1;
            padding-left:3px;
            padding-top:3px;
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
class VideoPRWidget(QWidget):

    def __init__(self, fwind):
        super().__init__()

        self.fWindow = fwind

        self.cap = None
        self.timer = None
        self.playState = PlayState.STOP
        self.videoType = None
        self.videoFile = None

        self.cap_frames_count = 0
        self.cap_currentframe = 0
        self.cap_fps = 0
        self.cap_width = 0
        self.cap_height = 0

        self.cvimg = None
        self.qimg = None
        self.platelist = []

        self.initUI()

    def initData(self):

        self.cap = None
        self.timer = None
        self.playState = PlayState.STOP
        self.videoType = None
        self.videoFile = None

        self.cap_frames_count = 0
        self.cap_currentframe = 0
        self.cap_fps = 0
        self.cap_width = 0
        self.cap_height = 0

        self.cvimg = None
        self.qimg = None
        self.platelist = []

    def initUI(self):
        self.setStyleSheet(MAIN_STYL)

        """-------------------- topLayout------------------------"""

        self.label_RunningMSG = QLabel()
        self.label_RunningMSG.setAlignment(Qt.AlignCenter)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.label_RunningMSG)

        """-------------------imgLabel-------------------------"""
        self.openLabel = QLabel()
        self.openLabel.setFixedSize(160, 52)

        self.btn_Open = QPushButton('打开', self.openLabel)
        self.btn_Open.setStyleSheet(BTN_STYL)
        self.btn_Open.setFixedSize(80, 40)
        self.btn_Open.move(0, 0)
        self.btn_Open.clicked.connect(self.on_btn_Open_clicked)

        self.combobox_Open = QComboBox(self.openLabel)
        self.combobox_Open.addItems(['本地文件', 'URL', '摄像头'])
        self.combobox_Open.setFixedSize(80, 40)
        self.combobox_Open.move(79, 0)
        self.combobox_Open.setStatusTip('设置视频类型')

        self.imglayout = QHBoxLayout()
        self.imglayout.setAlignment(Qt.AlignCenter)
        self.imglayout.addWidget(self.openLabel)

        self.imgLabel = VideoPRLabel(self)
        self.imgLabel.setAlignment(Qt.AlignCenter)
        self.imgLabel.setMaximumSize(10000, 10000)
        self.imgLabel.setStyleSheet("QLabel{background-color:black;}")
        self.imgLabel.setLayout(self.imglayout)

        """-------------------- videoOPlayout------------------------"""
        self.btn_Play = QPushButton('播放')
        self.btn_Play.setFixedSize(60,30)
        self.btn_Play.clicked.connect(self.playPlayer)

        self.btn_Pause = QPushButton('暂停')
        self.btn_Pause.setFixedSize(60, 30)
        self.btn_Pause.clicked.connect(self.pausePlayer)

        self.btn_Stop = QPushButton('停止')
        self.btn_Stop.setFixedSize(60, 30)
        self.btn_Stop.clicked.connect(self.stopPlayer)

        self.btn_LastFrame = QPushButton('<')
        self.btn_LastFrame.setFixedSize(30, 30)
        self.btn_LastFrame.clicked.connect(self.lastFrame)

        self.btn_NextFrame = QPushButton('>')
        self.btn_NextFrame.setFixedSize(30, 30)
        self.btn_NextFrame.clicked.connect(self.nextFrame)

        self.sld_Frame = QSlider(Qt.Horizontal)
        self.sld_Frame.setFixedHeight(30)
        self.sld_Frame.valueChanged[int].connect(self.frameSlidValueChange)

        self.videoOPlayout = QHBoxLayout()
        self.videoOPlayout.addWidget(self.btn_Play)
        self.videoOPlayout.addWidget(self.btn_Pause)
        self.videoOPlayout.addWidget(self.btn_Stop)
        self.videoOPlayout.addWidget(self.btn_LastFrame)
        self.videoOPlayout.addWidget(self.sld_Frame)
        self.videoOPlayout.addWidget(self.btn_NextFrame)

        self.videoOPlayout.setAlignment(Qt.AlignLeft)

        """-------------------- prOPlayout------------------------"""
        self.cb_Recognize = QCheckBox("识别")
        self.cb_Recognize.setStyleSheet(IOS_CHECKBOX_STYLE)

        self.label_RecognizeMSG = QLabel()
        self.label_RecognizeMSG.setAlignment(Qt.AlignCenter)

        self.prOPlayout = QHBoxLayout()
        self.prOPlayout.setAlignment(Qt.AlignLeft)

        self.prOPlayout.addWidget(self.cb_Recognize)
        self.prOPlayout.addWidget(self.label_RecognizeMSG)
        self.prOPlayout.setStretchFactor(self.label_RecognizeMSG, 1)

        """-------------------- prSetlayout------------------------"""
        self.cb_debug = QCheckBox("调试")
        self.cb_debug.setStyleSheet(IOS_CHECKBOX_STYLE)
        self.cb_label = QCheckBox("标注结果")
        self.cb_label.setStyleSheet(IOS_CHECKBOX_STYLE)

        self.label_DetectType = QLabel(' 检测类型')
        self.combobox_DetectType = QComboBox()
        self.combobox_DetectType.addItems(
            ['SOBEL', 'COLOR', 'CMSER', 'SOBEL&COLOR', 'SOBEL&CMSER', 'COLOR&CMSER', 'All'])
        self.combobox_DetectType.setStatusTip('设置检测类型')

        self.label_MaxPlates = QLabel(' 最大车牌数')
        self.spinbox_MaxPlates = QSpinBox()
        self.spinbox_MaxPlates.setFixedSize(50, 22)
        self.spinbox_MaxPlates.setAlignment(Qt.AlignCenter)
        self.spinbox_MaxPlates.setMinimum(1)
        self.spinbox_MaxPlates.setMaximum(10)
        self.spinbox_MaxPlates.setStatusTip('设置单帧检测车牌最大数量')

        self.prSetlayout = QHBoxLayout()
        self.prSetlayout.setAlignment(Qt.AlignLeft)

        self.prSetlayout.addWidget(self.cb_debug)
        self.prSetlayout.addWidget(self.cb_label)
        self.prSetlayout.addWidget(self.label_DetectType)
        self.prSetlayout.addWidget(self.combobox_DetectType)
        self.prSetlayout.addWidget(self.label_MaxPlates)
        self.prSetlayout.addWidget(self.spinbox_MaxPlates)
        self.prSetlayout.addStretch(1)

        """-------------------- vlayout------------------------"""
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.topLayout)
        self.vlayout.addWidget(self.imgLabel)
        self.vlayout.setStretchFactor(self.imgLabel, 1)
        self.vlayout.addLayout(self.videoOPlayout)
        self.vlayout.addLayout(self.prOPlayout)
        self.vlayout.addLayout(self.prSetlayout)

        self.setLayout(self.vlayout)

        self.initButton()

    def on_btn_Open_clicked(self):
        index = self.combobox_Open.currentIndex()

        if index == 0:

            self.videoFile = QFileDialog.getOpenFileName(self, "打开文件", "./resources/vidoe",
                                                         "视频文件(*.mp4 *.avi *.rmvb *.mkv *.flv)")[0]
            if len(self.videoFile) == 0:
                return
            if self.OpenVideo():
                self.videoType = VideoType.VIDEOFILE
                self.initPlayer()
                self.fWindow.statusBar().showMessage('视频打开成功!')
            else:
                self.fWindow.statusBar().showMessage('视频打开失败!')

        elif index == 1:
            self.videoFile, ok = QInputDialog.getText(self, 'URL', '输入URL:')
            if ok:
                if self.OpenVideo():
                    self.videoType = VideoType.URL
                    self.initPlayer()
                    self.fWindow.statusBar().showMessage('URL打开成功!')
                else:
                    self.fWindow.statusBar().showMessage('URL打开失败!')
        else:

            self.videoFile, ok = QInputDialog.getInt(self, '摄像头端口', '输入摄像头端口:', 0, 0, 100, 1)
            if ok:
                if self.OpenVideo():
                    self.videoType = VideoType.CAM
                    self.initPlayer()
                    self.fWindow.statusBar().showMessage('摄像头打开成功!')
                else:
                    self.fWindow.statusBar().showMessage('摄像头打开失败!')

    def OpenVideo(self):
        self.cap = cv2.VideoCapture(self.videoFile)
        if not self.cap.isOpened():
            return False
        return True

    def initButton(self):
        self.btn_Play.setEnabled(False)
        self.btn_Pause.setEnabled(False)
        self.btn_Stop.setEnabled(False)
        self.btn_LastFrame.setEnabled(False)
        self.btn_NextFrame.setEnabled(False)
        self.sld_Frame.setEnabled(False)
        self.sld_Frame.setValue(0)

    def initPlayer(self):

        self.cap_width = self.cap.get(3)
        self.cap_height = self.cap.get(4)
        self.cap_fps = 30

        self.btn_Pause.setEnabled(True)
        self.btn_Stop.setEnabled(True)

        if self.videoType == VideoType.VIDEOFILE:
            self.cap_fps = self.cap.get(5)
            self.cap_frames_count = self.cap.get(7)
            self.btn_LastFrame.setEnabled(True)
            self.btn_NextFrame.setEnabled(True)
            self.sld_Frame.setEnabled(True)
            self.sld_Frame.setMaximum(self.cap_frames_count)

        self.timer = QBasicTimer()
        self.timer.start(1000 / self.cap_fps, self)

        self.playState = PlayState.PLAY
        self.openLabel.hide()

    def stopPlayer(self):
        if self.cap.isOpened():
            self.cap.release()
        self.imgLabel.clear()
        self.openLabel.show()
        self.initButton()
        self.label_RunningMSG.setText('')
        self.label_RecognizeMSG.setText('')
        self.playState = PlayState.STOP
        self.timer.stop()

    def pausePlayer(self):
        if self.playState == PlayState.PLAY:
            self.playState = PlayState.PAUSE
            self.btn_Pause.setEnabled(False)
            self.btn_Play.setEnabled(True)

    def playPlayer(self):
        if self.playState == PlayState.PAUSE:
            self.playState = PlayState.PLAY
            self.btn_Play.setEnabled(False)
            self.btn_Pause.setEnabled(True)

    def updateFrame(self):
        ret, self.cvimg = self.cap.read()

        if ret:
            cvtemp = numpy.copy(self.cvimg)
            self.qimg = CV2QImage(self.cvimg)

            if self.cb_Recognize.isChecked():

                self.fWindow.plateRecognize.setDebug(self.cb_debug.isChecked())
                self.fWindow.plateRecognize.setDetectType(self.combobox_DetectType.currentIndex())
                self.fWindow.plateRecognize.setMaxPlates(self.spinbox_MaxPlates.value())

                begin = time()
                self.platelist = self.fWindow.plateRecognize.plateRecognize(cvtemp)
                end = time()
                runtime = end - begin

                if self.cb_label.isChecked():
                    for i in range(len(self.platelist)):
                        license, x, y, w, h = self.platelist[i]
                        cvtemp = cv2.rectangle(cvtemp, (x, y),
                                             (x + w, y + h), (0, 255, 0), 2)

                self.label_RecognizeMSG.setText(
                    '发现 {plates} 张车牌   运行时间:{runtime:.3f}s'.format(plates=len(self.platelist),
                                                                            runtime=runtime))

            qtemp = CV2QImage(cvtemp)
            self.imgLabel.setPixmap(QPixmap.fromImage(qtemp))

            if self.videoType == VideoType.VIDEOFILE:
                self.cap_currentframe = self.cap.get(1)
                self.sld_Frame.setValue(self.cap_currentframe)

            self.label_RunningMSG.setText(
                '帧数:{current_frame}/{frames_count}  FPS:{fps}   宽:{width}    高:{height}'.format( \
                    current_frame=self.cap_currentframe, \
                    frames_count=self.cap_frames_count, \
                    fps=self.cap_fps, \
                    width=self.cap_width, \
                    height=self.cap_height))

    def frameSlidValueChange(self, value):
        if value != self.cap_currentframe:
            self.cap_currentframe = value
            self.cap.set(1, self.cap_currentframe)
            self.updateFrame()

    def lastFrame(self):
        if self.cap_currentframe > 0:
            self.sld_Frame.setValue(self.cap_currentframe - 2)
            self.pausePlayer()

    def nextFrame(self):
        if self.cap_currentframe < self.cap_frames_count - 3:
            self.sld_Frame.setValue(self.cap_currentframe + 1)
            self.pausePlayer()

    def hide(self):
        if self.playState != PlayState.STOP:
            self.timer.stop()
            self.stopPlayer()
        super().hide()

    def show(self):
        self.openLabel.show()
        self.initData()
        super().show()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():

            if self.playState == PlayState.PLAY:
                self.updateFrame()

            if self.videoType == VideoType.VIDEOFILE and self.cap_currentframe > self.cap_frames_count - 3:
                self.stopPlayer()

        else:
            super().timerEvent(event)

    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Space:
            if self.playState == PlayState.PLAY:
                self.pausePlayer()
            elif self.playState == PlayState.PAUSE:
                self.playPlayer()
            return

        if key == Qt.Key_Left:
            if self.playState != PlayState.STOP and self.videoType == VideoType.VIDEOFILE:
                self.lastFrame()
            return

        if key == Qt.Key_Right:
            if self.playState != PlayState.STOP and self.videoType == VideoType.VIDEOFILE:
                self.nextFrame()
            return

        super().keyPressEvent(event)
