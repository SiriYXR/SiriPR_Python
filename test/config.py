# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:config.py
@time:2018/8/8 14:50
"""
from enum import Enum

class Color(Enum):
    BLUE = 0
    YELLOW = 1
    WHITE = 2
    UNKNOWN = 3

class DetectType(Enum):
    SOBEL=0
    COLOR=1
    CMSER=2
    OTHER=3

class CharSearchDirection(Enum):
    LEFT=0
    RIGHT=1