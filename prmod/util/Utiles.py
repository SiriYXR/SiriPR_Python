# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:Utiles.py
@time:2018/9/22 16:47
"""
import ctypes
import inspect

import cv2

import numpy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QImage, qRed, qGreen, qBlue, QPainter, QColor, QFont, QPixmap
from PyQt5.QtWidgets import QComboBox, QLabel


def cv_imread(filePath="", flags=0):
    cv_img = cv2.imdecode(numpy.fromfile(filePath, dtype=numpy.uint8), flags)
    return cv_img


def CV2QImage(cv_image):
    height, width, bytesPerComponent = cv_image.shape
    bytesPerLine = 3 * width
    cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB, cv_image)
    qimg = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888)

    return qimg


def QImage2CV(qimg):
    tmp = qimg

    # 使用numpy创建空的图象
    cv_image = numpy.zeros((tmp.height(), tmp.width(), 3), dtype=numpy.uint8)

    for row in range(0, tmp.height()):
        for col in range(0, tmp.width()):
            r = qRed(tmp.pixel(col, row))
            g = qGreen(tmp.pixel(col, row))
            b = qBlue(tmp.pixel(col, row))
            cv_image[row, col, 0] = r
            cv_image[row, col, 1] = g
            cv_image[row, col, 2] = b

    return cv_image


class MyComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()  # 创建一个信号

    def __init__(self, parent=None):
        super(MyComboBox, self).__init__(parent)

    def showPopup(self):  # 重写showPopup函数
        self.popupAboutToBeShown.emit()  # 发送信号
        QComboBox.showPopup(self)  # 弹出选项框


class VideoPRLabel(QLabel):

    def __init__(self, parent):
        super().__init__()

        self.Parent = parent

    def paintEvent(self, event):

        super().paintEvent(event)

        if len(self.Parent.platelist) != 0:
            painter = QPainter()
            painter.begin(self)
            self.drawPlate(painter)
            painter.end()

    def drawPlate(self, painter):

        for i in range(len(self.Parent.platelist)):
            license, x, y, w, h = self.Parent.platelist[i]
            print(license)
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(0, 30 * i, 110, 30)

            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Microsoft YaHei", 10, QFont.Normal))
            painter.drawText(10, 30 * i+20, license)

            plateimg = self.Parent.qimg.copy(x, y, w, h).scaled(140, 30)
            painter.drawPixmap(110, 30 * i, QPixmap.fromImage(plateimg))


"""强制终止线程"""
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        """if it returns a number greater than one, you're in trouble,
        and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def TickTimeProcess(t):
    if t <60:
        return '{:.2f}秒'.format(t)
    elif t<60*60:
        i=int(t)
        m=i/60
        s=t-m*60
        return '{}分 {:.2f}秒'.format(m,s)
    else:
        i = int(t)
        h = i/(60*60)
        m = (i-h*60*60)/60
        s = t - m * 60-h*60*60
        return '{}小时 {}分 {:.2f}秒'.format(h,m,s)