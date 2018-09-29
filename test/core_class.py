# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:core_class.py
@time:2018/8/8 16:11
"""

class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class Rect:

    def __init__(self,x=0,y=0,w=0,h=0,angl=0):
       self.x=x
       self.y=y
       self.width=w
       self.height=h
       self.angl=angl

    def getPoint(self):
        return Point(self.x,self.y)