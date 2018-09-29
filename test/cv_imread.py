# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:cv_imread.py
@time:2018/8/1 17:23
"""
import numpy as np
import cv2 as cv

def cv_imread(filePath = "",flags= 0):
    cv_img = cv.imdecode(np.fromfile(filePath, dtype=np.uint8), flags)
    return cv_img
