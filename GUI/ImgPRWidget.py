# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:ImgPRWidget.py
@time:2018/9/22 15:38
"""
from time import time

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QCheckBox, QHBoxLayout, QScrollArea, \
    QSpinBox

from prmod.core.CPlate import CPlate
from prmod.util.Utiles import *


class ImgPRWidget(QWidget):

    def __init__(self, fwind):
        super().__init__()

        self.fWindow = fwind
        self.cvimg = None
        self.qimg = None
        self.plate = None
        self.filelist = None
        self.platelist = None
        self.fileindex = -1
        self.plateindex = -1

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

        """--------------------------------------------"""
        self.imgLabel = QLabel("Add an image file ")
        self.imgLabel.setAlignment(Qt.AlignCenter)

        self.sa_img = QScrollArea()
        self.sa_img.setWidget(self.imgLabel)
        self.sa_img.setAlignment(Qt.AlignCenter)

        """-------------------- imgListlayout------------------------"""
        self.combobox_File = MyComboBox()
        self.combobox_File.popupAboutToBeShown.connect(self.on_combobox_File_clicked)

        self.btn_last_img = QPushButton("<")
        self.btn_last_img.setFixedSize(30, 30)
        self.btn_last_img.setStatusTip('Load the last image')
        self.btn_last_img.clicked.connect(self.on_btn_last_img_clicked)

        self.btn_next_img = QPushButton(">")
        self.btn_next_img.setFixedSize(30, 30)
        self.btn_next_img.setStatusTip('Load the next image')
        self.btn_next_img.clicked.connect(self.on_btn_next_img_clicked)

        self.imgListlayout = QHBoxLayout()
        self.imgListlayout.addWidget(self.btn_last_img)
        self.imgListlayout.addWidget(self.combobox_File)
        self.imgListlayout.addWidget(self.btn_next_img)

        """--------------------fileOPlayout------------------------"""
        self.btn_open = QPushButton("Open")
        self.btn_open.setStatusTip('Open image files')
        self.btn_open.clicked.connect(self.on_btn_open_clicked)

        self.fileOPlayout = QHBoxLayout()
        self.fileOPlayout.addWidget(self.btn_open)

        """--------------------prOPlayout------------------------"""
        self.btn_recognize = QPushButton("Recognize")
        self.btn_recognize.setFixedWidth(100)
        self.btn_recognize.setStatusTip('Recongnize current image')
        self.btn_recognize.clicked.connect(self.on_btn_recognize_clicked)

        self.resLabel = QLabel("")
        self.resLabel.setAlignment(Qt.AlignCenter)
        self.resLabel.setFixedHeight(30)

        self.combobox_Plate = MyComboBox()
        self.combobox_Plate.popupAboutToBeShown.connect(self.on_combobox_Plate_clicked)

        self.btn_last_plate = QPushButton("<")
        self.btn_last_plate.setFixedSize(30, 30)
        self.btn_last_plate.setStatusTip('Turn to the last plate')
        self.btn_last_plate.clicked.connect(self.on_btn_last_plate_clicked)

        self.btn_next_plate = QPushButton(">")
        self.btn_next_plate.setFixedSize(30, 30)
        self.btn_next_plate.setStatusTip('Turn to the next plate')
        self.btn_next_plate.clicked.connect(self.on_btn_next_plate_clicked)

        self.prOPlayout = QHBoxLayout()
        self.prOPlayout.addWidget(self.btn_recognize)
        self.prOPlayout.addWidget(self.btn_last_plate)
        self.prOPlayout.addWidget(self.combobox_Plate)
        self.prOPlayout.addWidget(self.btn_next_plate)

        """--------------------setinglayout------------------------"""
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

        self.setinglayout = QHBoxLayout()
        self.setinglayout.addWidget(self.cb_debug)
        self.setinglayout.addWidget(self.cb_label)
        self.setinglayout.addWidget(self.label_DetectType)
        self.setinglayout.addWidget(self.combobox_DetectType)
        self.setinglayout.addWidget(self.label_MaxPlates)
        self.setinglayout.addWidget(self.spinbox_MaxPlates)
        self.setinglayout.addStretch(1)

        """--------------------vlayout------------------------"""
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.topLayout)
        self.vlayout.addWidget(self.sa_img)
        self.vlayout.addLayout(self.imgListlayout)
        self.vlayout.addLayout(self.fileOPlayout)
        self.vlayout.addLayout(self.prOPlayout)
        self.vlayout.addLayout(self.setinglayout)

        self.setLayout(self.vlayout)

    @pyqtSlot(bool)
    def on_btn_return_clicked(self, checked):
        self.fWindow.on_indexAct_clicked()

    def on_combobox_File_clicked(self):
        if self.fileindex == -1:
            return
        self.fileindex = self.combobox_File.currentIndex()
        self.openIMG(self.filelist[self.fileindex])

    @pyqtSlot(bool)
    def on_btn_last_img_clicked(self, checked):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('Please open image first!')
            return
        if self.fileindex == 0:
            self.fWindow.statusBar().showMessage('It\'s the first image!')
            return

        self.fileindex -= 1
        self.combobox_File.setCurrentIndex(self.fileindex)
        self.on_combobox_File_clicked()

    @pyqtSlot(bool)
    def on_btn_next_img_clicked(self, checked):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('Please open image first!')
            return
        if self.fileindex == len(self.filelist) - 1:
            self.fWindow.statusBar().showMessage('It\'s the last image!')
            return

        self.fileindex += 1
        self.combobox_File.setCurrentIndex(self.fileindex)
        self.on_combobox_File_clicked()

    @pyqtSlot(bool)
    def on_btn_open_clicked(self, checked):
        self.filelist = QFileDialog.getOpenFileNames(self, "OpenFile", "./resources/image",
                                                     "Image Files(*.jpg *.jpeg *.png)")[0]
        if len(self.filelist):
            self.combobox_File.clear()
            for i in range(len(self.filelist)):
                self.combobox_File.insertItem(i, self.filelist[i] + " ({index}/{all})".format(index=i + 1,
                                                                                              all=len(self.filelist)))
            self.fileindex = 0
            self.openIMG(self.filelist[self.fileindex])

    @pyqtSlot(bool)
    def on_btn_recognize_clicked(self, checked):

        if self.qimg != None:
            self.plate = CPlate()
            self.label_RunningMSG.setText('Image recongnizing...')

            self.fWindow.plateRecognize.setDebug(self.cb_debug.isChecked())
            self.fWindow.plateRecognize.setDetectType(self.combobox_DetectType.currentIndex())
            self.fWindow.plateRecognize.setMaxPlates(self.spinbox_MaxPlates.value())

            begin = time()
            self.platelist = self.fWindow.plateRecognize.plateRecognize(numpy.copy(self.cvimg))
            end = time()
            runtime = end - begin

            platenum = len(self.platelist)

            if platenum != 0:
                self.plateindex = 0
                self.combobox_Plate.clear()
                for i in range(platenum):
                    self.plate.license, self.plate.x, self.plate.y, self.plate.w, self.plate.h = self.platelist[i]
                    self.combobox_Plate.insertItem(i, "{p.license} {p.x} {p.y} {p.w} {p.h}".format(p=self.plate))

                self.label_RunningMSG.setText(
                    'Image recongnize finished.     Found {plates} plate.    Runtime:{runtime:.3f}s'.format(
                        plates=platenum, runtime=runtime))

                self.setShowPlate()
            else:
                self.label_RunningMSG.setText('Not found plate!')
        else:
            self.fWindow.statusBar().showMessage('Please open image first!')

    def on_combobox_Plate_clicked(self):
        if self.plateindex == -1:
            return
        self.plateindex = self.combobox_Plate.currentIndex()
        self.setShowPlate()

    @pyqtSlot(bool)
    def on_btn_next_plate_clicked(self, checked):
        if self.plateindex == -1:
            self.fWindow.statusBar().showMessage('Have no plates!')
            return

        if self.plateindex == len(self.platelist) - 1:
            self.fWindow.statusBar().showMessage('It\'s the last plate!')
            return

        self.plateindex += 1
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.on_combobox_Plate_clicked()

    @pyqtSlot(bool)
    def on_btn_last_plate_clicked(self, checked):
        if self.plateindex == -1:
            self.fWindow.statusBar().showMessage('Have no plates!')
            return

        if self.plateindex == 0:
            self.fWindow.statusBar().showMessage('It\'s the first plate!')
            return

        self.plateindex -= 1
        self.combobox_Plate.setCurrentIndex(self.plateindex)
        self.on_combobox_Plate_clicked()

    def initButton(self):
        self.label_RunningMSG.clear()
        self.imgLabel.clear()
        self.imgLabel.setText('Add an image file ')
        self.combobox_File.clear()
        self.combobox_Plate.clear()
        self.combobox_DetectType.setCurrentIndex(0)
        self.spinbox_MaxPlates.setValue(1)
        self.cb_debug.setCheckState(False)
        self.cb_label.setCheckState(False)

    def show(self):
        self.initButton()
        super().show()

    def openIMG(self, filename):
        self.cvimg = cv_imread(filename, 1)
        self.qimg = CV2QImage(numpy.copy(self.cvimg))
        self.setShowIMG(self.cvimg)
        if (self.qimg != None):
            self.fWindow.statusBar().showMessage('Image open success.')
        else:
            self.fWindow.statusBar().showMessage('Image open failed.')

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
