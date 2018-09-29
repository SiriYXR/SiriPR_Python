# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:VideoPRWidget.py
@time:2018/9/26 12:08
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

        """-------------------imgLabel-------------------------"""
        self.openLabel = QLabel()
        self.openLabel.setFixedSize(160, 52)

        self.btn_Open = QPushButton('Open', self.openLabel)
        self.btn_Open.setFixedSize(80, 42)
        self.btn_Open.move(0, 0)
        self.btn_Open.clicked.connect(self.on_btn_Open_clicked)

        self.combobox_Open = QComboBox(self.openLabel)
        self.combobox_Open.addItems(['File', 'URL', 'Camera'])
        self.combobox_Open.setFixedSize(80, 40)
        self.combobox_Open.move(79, 1)
        self.combobox_Open.setStatusTip('Set the video type')

        self.imglayout = QHBoxLayout()
        self.imglayout.setAlignment(Qt.AlignCenter)
        self.imglayout.addWidget(self.openLabel)

        self.imgLabel = VideoPRLabel(self)
        self.imgLabel.setAlignment(Qt.AlignCenter)
        self.imgLabel.setMaximumSize(10000, 10000)
        self.imgLabel.setStyleSheet("QLabel{background-color:black;}")
        self.imgLabel.setLayout(self.imglayout)

        """-------------------- videoOPlayout------------------------"""
        self.btn_Play = QPushButton('Play')
        self.btn_Play.clicked.connect(self.playPlayer)

        self.btn_Pause = QPushButton('Pause')
        self.btn_Pause.clicked.connect(self.pausePlayer)

        self.btn_Stop = QPushButton('Stop')
        self.btn_Stop.clicked.connect(self.stopPlayer)

        self.btn_LastFrame = QPushButton('<')
        self.btn_LastFrame.setFixedWidth(30)
        self.btn_LastFrame.clicked.connect(self.lastFrame)

        self.btn_NextFrame = QPushButton('>')
        self.btn_NextFrame.setFixedWidth(30)
        self.btn_NextFrame.clicked.connect(self.nextFrame)

        self.sld_Frame = QSlider(Qt.Horizontal)
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
        self.cb_Recognize = QCheckBox("Recognize")

        self.label_RecognizeMSG = QLabel()
        self.label_RecognizeMSG.setAlignment(Qt.AlignCenter)

        self.prOPlayout = QHBoxLayout()
        self.prOPlayout.setAlignment(Qt.AlignLeft)

        self.prOPlayout.addWidget(self.cb_Recognize)
        self.prOPlayout.addWidget(self.label_RecognizeMSG)
        self.prOPlayout.setStretchFactor(self.label_RecognizeMSG, 1)

        """-------------------- prSetlayout------------------------"""
        self.cb_debug = QCheckBox("Debug")
        self.cb_label = QCheckBox("Label")

        self.label_DetectType = QLabel(' DetectType')
        self.combobox_DetectType = QComboBox()
        self.combobox_DetectType.addItems(
            ['SOBEL', 'COLOR', 'CMSER', 'SOBEL&COLOR', 'SOBEL&CMSER', 'COLOR&CMSER', 'All'])
        self.combobox_DetectType.setStatusTip('Set the detect type')

        self.label_MaxPlates = QLabel(' MaxPlates')
        self.spinbox_MaxPlates = QSpinBox()
        self.spinbox_MaxPlates.setMinimum(1)
        self.spinbox_MaxPlates.setMaximum(10)
        self.spinbox_MaxPlates.setStatusTip('Set the number of max plates')

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

    @pyqtSlot(bool)
    def on_btn_return_clicked(self, checked):
        self.fWindow.on_indexAct_clicked()

    def on_btn_Open_clicked(self):
        index = self.combobox_Open.currentIndex()

        if index == 0:

            self.videoFile = QFileDialog.getOpenFileName(self, "OpenFile", "./resources/vidoe",
                                                         "Video File(*.mp4 *.avi *.rmvb *.mkv *.flv)")[0]
            if len(self.videoFile) == 0:
                return
            if self.OpenVideo():
                self.videoType = VideoType.VIDEOFILE
                self.initPlayer()
                self.fWindow.statusBar().showMessage('Video open success!')
            else:
                self.fWindow.statusBar().showMessage('Video open faild!')

        elif index == 1:
            self.videoFile, ok = QInputDialog.getText(self, 'URL', 'Input the URL:')
            if ok:
                if self.OpenVideo():
                    self.videoType = VideoType.URL
                    self.initPlayer()
                    self.fWindow.statusBar().showMessage('URL open success!')
                else:
                    self.fWindow.statusBar().showMessage('URL open faild!')
        else:

            self.videoFile, ok = QInputDialog.getInt(self, 'Camera Port', 'Input the camera port:', 0, 0, 100, 1)
            if ok:
                if self.OpenVideo():
                    self.videoType = VideoType.CAM
                    self.initPlayer()
                    self.fWindow.statusBar().showMessage('Camera open success!')
                else:
                    self.fWindow.statusBar().showMessage('Camera open faild!')

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
                    'Found {plates} plate.   Runtime:{runtime:.3f}s'.format(plates=len(self.platelist),
                                                                            runtime=runtime))

            qtemp = CV2QImage(cvtemp)
            self.imgLabel.setPixmap(QPixmap.fromImage(qtemp))

            if self.videoType == VideoType.VIDEOFILE:
                self.cap_currentframe = self.cap.get(1)
                self.sld_Frame.setValue(self.cap_currentframe)

            self.label_RunningMSG.setText(
                'Frames:{current_frame}/{frames_count}  FPS:{fps}   Width:{width}    Height:{height}'.format( \
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

        if key == Qt.Key_Escape:
            self.fWindow.on_indexAct_clicked()
            return

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
