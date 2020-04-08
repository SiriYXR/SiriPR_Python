# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:ImgOutPortWidget.py
@time:2020/4/8 13:03
"""

import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog,QWidget, QHBoxLayout,QVBoxLayout, QPushButton,QRadioButton,QLabel,QProgressBar

from prmod.util.Utiles import *

MAIN_STYLE="""
        QDialog{
            background:#FBFAFA;
        }
        
        QLabel{
            font-family:Microsoft Yahei;
            font-size:15px;
            color:dimgray;
        }
        """

IOS_RADIOBTN_STYLE="""
        /*RadioButton样式设置*/
        QRadioButton::indicator { 
            width: 17px;
            height: 17px;
        }
        /*单选框未选中样式*/
        QRadioButton::indicator::unchecked {
             
            image: url(GUI2/img/unchecked_radiobutton.png);
        }
        /*单选框选中样式*/
        QRadioButton::indicator::checked { 
            image: url(GUI2/img/checked_radiobutton.png);
        }
        /*RadioButton和checkbox字体和间距设置*/
        QRadioButton{
            spacing: 5px;
            font-size: 13px;
        }
        """

class OutportImgThread(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self,fwind,pattern):
        super(OutportImgThread, self).__init__()
        self.fwind=fwind
        self.pattern=pattern

        self.cancell=False

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(len(self.fwind.checkedlist)):

            self.fwind.outPutImg(self.fwind.checkedlist[i],self.pattern)

            self._signal.emit(str(i))  # 注意这里与_signal = pyqtSignal(str)中的类型相同

            if self.cancell:
                return

        self._signal.emit('end')



class ImgOutPortWidget(QDialog):

    def __init__(self, fWind):
        super().__init__(fWind)
        self.fWindow=fWind

        self.thread=None
        self.tick=0

        self.initUI()

    def initUI(self):
        self.setStyleSheet(MAIN_STYLE+IOS_RADIOBTN_STYLE)

        self.setWindowTitle('图片识别结果导出')
        self.setFixedSize(300,200)

        """------------------layout_setting-------------------"""
        layout_setting=QVBoxLayout()
        layout_setting.setContentsMargins(0,0,0,0)
        layout_setting.setSpacing(0)
        layout_setting.setAlignment(Qt.AlignCenter)

        self.settingLabel=QLabel("设置识别操作执行策略")
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLabel.setFixedHeight(20)

        self.radioButton1 = QRadioButton('全部重新识别')
        self.radioButton1.setChecked(True)
        self.radioButton2 = QRadioButton('已有识别结果的直接保存')
        self.radioButton2.setFixedWidth(200)

        layout_radio=QHBoxLayout()
        layout_radio.setContentsMargins(10, 0, 0, 0)
        layout_radio.setSpacing(10)
        layout_radio.addWidget(self.radioButton1)
        layout_radio.addWidget(self.radioButton2)

        self.startBtn=QPushButton('开始')
        self.startBtn.setFixedSize(300,30)
        self.startBtn.clicked.connect(self.on_startBtn_clicked)

        layout_setting.addStretch(2)
        layout_setting.addWidget(self.settingLabel)
        layout_setting.addStretch(2)
        layout_setting.addLayout(layout_radio)
        layout_setting.addStretch(3)
        layout_setting.addWidget(self.startBtn)

        """------------------layout_process-------------------"""
        layout_process=QVBoxLayout()
        layout_process.setContentsMargins(0, 0, 0, 0)
        layout_process.setSpacing(0)


        self.processLabel=QLabel("导出：")


        self.progressBar=QProgressBar()
        self.progressBar.setFixedSize(260,30)
        self.progressBar.setValue(0)

        layout_progress=QVBoxLayout()
        layout_progress.setContentsMargins(20, 0, 0, 0)
        layout_progress.setSpacing(5)
        layout_progress.addWidget(self.processLabel)
        layout_progress.addWidget(self.progressBar)

        self.cancellBtn=QPushButton("取消")
        self.cancellBtn.setFixedSize(300, 30)
        self.cancellBtn.clicked.connect(self.on_cancellBtn_clicked)

        layout_process.addStretch(3)
        layout_process.addLayout(layout_progress)
        layout_process.addStretch(3)
        layout_process.addWidget(self.cancellBtn)

        """------------------layout_end-------------------"""
        layout_end = QVBoxLayout()
        layout_end.setContentsMargins(0, 0, 0, 0)
        layout_end.setSpacing(0)

        self.endLabel = QLabel("导出结束")
        self.endLabel.setAlignment(Qt.AlignCenter)

        self.endBtn = QPushButton("完成")
        self.endBtn.setFixedSize(300,30)
        self.endBtn.clicked.connect(self.on_endBtn_clicked)

        layout_end.addWidget(self.endLabel)
        layout_end.addWidget(self.endBtn)

        self.settingWidget=QWidget(self)
        self.settingWidget.setFixedSize(300,200)
        self.settingWidget.setHidden(False)
        self.settingWidget.setLayout(layout_setting)

        self.processWidget=QWidget(self)
        self.processWidget.setFixedSize(300, 200)
        self.processWidget.setHidden(True)
        self.processWidget.setLayout(layout_process)

        self.endWidget=QWidget(self)
        self.endWidget.setFixedSize(300, 200)
        self.endWidget.setHidden(True)
        self.endWidget.setLayout(layout_end)


        self.exec()

    def on_startBtn_clicked(self):
        self.tick=time.time()
        self.settingWidget.setHidden(True)
        self.processWidget.setHidden(False)

        pattern=0
        if self.radioButton2.isChecked():
            pattern=1

        # 创建线程
        self.thread = OutportImgThread(self.fWindow,pattern)
        # 连接信号
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    def on_cancellBtn_clicked(self):
        self.thread.cancell = True
        self.close()

    def on_endBtn_clicked(self):
        self.close()

    def call_backlog(self, msg):
        if msg == 'end':
            del self.thread
            cost_time=time.time()-self.tick
            self.endLabel.setText("导出结束\n用时:"+TickTimeProcess(cost_time))
            self.processWidget.setHidden(True)
            self.endWidget.setHidden(False)
            return

        checked_index=int(msg)
        checked_length=len(self.fWindow.checkedlist)
        file_index = self.fWindow.checkedlist[checked_index]
        file_name = self.fWindow.filelist[file_index].file_name
        self.processLabel.setText("导出：" + file_name)
        self.progressBar.setValue(int((checked_index+1)/checked_length*100))  # 将线程的参数传入进度条
