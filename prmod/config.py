# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:config.py
@time:2018/8/8 14:50
"""

from enum import Enum

"""---------DetectType----------"""
PR_DETECT_SOBEL=0
PR_DETECT_COLOR=1
PR_DETECT_CMSER=2
PR_DETECT_SOBEL_COLOR=3
PR_DETECT_SOBEL_CMSER=4
PR_DETECT_COLOR_CMSER=5
PR_DETECT_SOBEL_COLOR_CMSER=6


class PlayState(Enum):
    PLAY = 0
    PAUSE = 1
    STOP = 2


class VideoType(Enum):
    VIDEOFILE = 0
    URL = 1
    CAM = 2