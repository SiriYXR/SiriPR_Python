# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:SettingWidget.py
@time:2018/9/24 14:29
"""
import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFileDialog, \
    QPushButton, QScrollArea


class SettingWidget(QDialog):

    def __init__(self, fWind):
        super().__init__(fWind)
        self.fWindow=fWind
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 400)
        self.move((QApplication.desktop().width() - self.width()) / 2,
                  (QApplication.desktop().height() - self.height()) / 2)
        self.setWindowTitle('Settings')

        self.config = configparser.ConfigParser()

        self.config.read("resources/config/siripr.ini")

        self.label_ModelPath=QLabel('Set Path')
        self.label_ModelPath.setFixedHeight(30)
        self.label_ModelPath.setAlignment(Qt.AlignCenter)

        self.label_SVM = QLabel('SVM Path:')
        self.label_SVM.setFixedWidth(120)
        self.label_SVM.setAlignment(Qt.AlignRight)
        self.lineedit_SVM = QLineEdit(self.config.get('Model', 'SVM'))
        self.btn_SVM = QPushButton('...')
        self.btn_SVM.setFixedWidth(30)
        self.btn_SVM.clicked.connect(self.on_btn_SVM_clicked)

        self.layout_SVM = QHBoxLayout()
        self.layout_SVM.addWidget(self.label_SVM)
        self.layout_SVM.addWidget(self.lineedit_SVM)
        self.layout_SVM.addWidget(self.btn_SVM)

        self.label_ANN = QLabel('ANN Path:')
        self.label_ANN.setFixedWidth(120)
        self.label_ANN.setAlignment(Qt.AlignRight)
        self.lineedit_ANN = QLineEdit(self.config.get('Model', 'ANN'))
        self.btn_ANN = QPushButton('...')
        self.btn_ANN.setFixedWidth(30)
        self.btn_ANN.clicked.connect(self.on_btn_ANN_clicked)

        self.layout_ANN = QHBoxLayout()
        self.layout_ANN.addWidget(self.label_ANN)
        self.layout_ANN.addWidget(self.lineedit_ANN)
        self.layout_ANN.addWidget(self.btn_ANN)

        self.label_ChineseANN = QLabel('ChineseANN Path:')
        self.label_ChineseANN.setFixedWidth(120)
        self.label_ChineseANN.setAlignment(Qt.AlignRight)
        self.lineedit_ChineseANN = QLineEdit(self.config.get('Model', 'ChineseANN'))
        self.btn_ChineseANN = QPushButton('...')
        self.btn_ChineseANN.setFixedWidth(30)
        self.btn_ChineseANN.clicked.connect(self.on_btn_ChineseANN_clicked)

        self.layout_ChineseANN = QHBoxLayout()
        self.layout_ChineseANN.addWidget(self.label_ChineseANN)
        self.layout_ChineseANN.addWidget(self.lineedit_ChineseANN)
        self.layout_ChineseANN.addWidget(self.btn_ChineseANN)

        self.label_GrayChANN = QLabel('GrayChANN Path:')
        self.label_GrayChANN.setFixedWidth(120)
        self.label_GrayChANN.setAlignment(Qt.AlignRight)
        self.lineedit_GrayChANN = QLineEdit(self.config.get('Model', 'GrayChANN'))
        self.btn_GrayChANN = QPushButton('...')
        self.btn_GrayChANN.setFixedWidth(30)
        self.btn_GrayChANN.clicked.connect(self.on_btn_GrayChANN_clicked)

        self.layout_GrayChANN = QHBoxLayout()
        self.layout_GrayChANN.addWidget(self.label_GrayChANN)
        self.layout_GrayChANN.addWidget(self.lineedit_GrayChANN)
        self.layout_GrayChANN.addWidget(self.btn_GrayChANN)

        self.label_ChineseMapping = QLabel('ChineseMapping Path:')
        self.label_ChineseMapping.setFixedWidth(120)
        self.label_ChineseMapping.setAlignment(Qt.AlignRight)
        self.lineedit_ChineseMapping = QLineEdit(self.config.get('Model', 'ChineseMapping'))
        self.btn_ChineseMapping = QPushButton('...')
        self.btn_ChineseMapping.setFixedWidth(30)
        self.btn_ChineseMapping.clicked.connect(self.on_btn_ChineseMapping_clicked)

        self.layout_ChineseMapping = QHBoxLayout()
        self.layout_ChineseMapping.addWidget(self.label_ChineseMapping)
        self.layout_ChineseMapping.addWidget(self.lineedit_ChineseMapping)
        self.layout_ChineseMapping.addWidget(self.btn_ChineseMapping)

        self.layout_Settings=QVBoxLayout()
        self.layout_Settings.addWidget(self.label_ModelPath)
        self.layout_Settings.addLayout(self.layout_SVM)
        self.layout_Settings.addLayout(self.layout_ANN)
        self.layout_Settings.addLayout(self.layout_ChineseANN)
        self.layout_Settings.addLayout(self.layout_GrayChANN)
        self.layout_Settings.addLayout(self.layout_ChineseMapping)

        self.sa_Settings = QScrollArea()
        self.sa_Settings.setLayout(self.layout_Settings)
        self.sa_Settings.setAlignment(Qt.AlignHCenter)

#------------------------------------------------------
        self.btn_ok = QPushButton('OK')
        self.btn_ok.clicked.connect(self.on_btn_ok_clicked)
        self.btn_cancel = QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.on_btn_cancel_clicked)
        self.btn_apply = QPushButton('Apply')
        self.btn_apply.clicked.connect(self.on_btn_apply_clicked)

        self.layout_bottom = QHBoxLayout()
        self.layout_bottom.addStretch(1)
        self.layout_bottom.addWidget(self.btn_ok)
        self.layout_bottom.addWidget(self.btn_cancel)
        self.layout_bottom.addWidget(self.btn_apply)

#-------------------------------------------------------
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.sa_Settings)
        self.vLayout.addLayout(self.layout_bottom)

        self.setLayout(self.vLayout)

        self.exec()

    def on_btn_SVM_clicked(self):
        path = QFileDialog.getOpenFileName(self, "Setting SVM model path", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_SVM.setText(path)

    def on_btn_ANN_clicked(self):
        path = QFileDialog.getOpenFileName(self, "Setting ANN model path", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_ANN.setText(path)

    def on_btn_ChineseANN_clicked(self):
        path = QFileDialog.getOpenFileName(self, "Setting ChineseANN model path", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_ChineseANN.setText(path)

    def on_btn_GrayChANN_clicked(self):
        path = QFileDialog.getOpenFileName(self, "Setting GrayChANN model path", "./resources/model",
                                           "Model File(*.xml)")[0]
        if len(path) != 0:
            self.lineedit_GrayChANN.setText(path)

    def on_btn_ChineseMapping_clicked(self):
        path = QFileDialog.getOpenFileName(self, "Setting ChineseMapping model path", "./resources/model",
                                           "File(*)")[0]
        if len(path) != 0:
            self.lineedit_ChineseMapping.setText(path)

    def on_btn_ok_clicked(self):
        self.saveConfig()
        self.close()

    def on_btn_cancel_clicked(self):
        self.close()

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