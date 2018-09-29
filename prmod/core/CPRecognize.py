# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:CPRecognize.py
@time:2018/9/23 16:34
"""
import configparser

from siripyd.siripr import CPlateRecognize

from prmod.config import *


class CPRecognize():

    def __init__(self, lifemod=1, debug=0):
        self.PR = CPlateRecognize()
        self.setLifemode(lifemod)
        self.setDetectType(PR_DETECT_COLOR)
        self.setMaxPlates(1)
        self.setDebug(debug)
        self.loadModel()

    def loadModel(self):
        config = configparser.ConfigParser()

        config.read("resources/config/siripr.ini")

        self.PR.LoadANN(config.get('Model', 'ANN'))
        self.PR.LoadSVM(config.get('Model', 'SVM'))
        self.PR.LoadChineseANN(config.get('Model', 'ChineseANN'))
        self.PR.LoadGrayChANN(config.get('Model', 'GrayChANN'))
        self.PR.LoadChineseMapping(config.get('Model', 'ChineseMapping'))

    def plateRecognize(self, src):
        return self.PR.plateRecognize(src)

    def setDetectType(self, type):
        if type == 0:
            self.PR.setDetectType(PR_DETECT_SOBEL)
        elif type == 1:
            self.PR.setDetectType(PR_DETECT_COLOR)
        elif type == 2:
            self.PR.setDetectType(PR_DETECT_CMSER)
        elif type == 3:
            self.PR.setDetectType(PR_DETECT_SOBEL_COLOR)
        elif type == 4:
            self.PR.setDetectType(PR_DETECT_SOBEL_CMSER)
        elif type == 5:
            self.PR.setDetectType(PR_DETECT_COLOR_CMSER)
        elif type == 6:
            self.PR.setDetectType(PR_DETECT_SOBEL_COLOR_CMSER)

    def setMaxPlates(self, param):
        self.PR.setMaxPlates(param)

    def setLifemode(self, param):
        self.PR.setLifemode(param)

    def setDebug(self, debug):
        self.PR.setDebug(debug)
