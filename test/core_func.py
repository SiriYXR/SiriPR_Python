# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:core_func.py
@time:2018/8/8 15:33
"""

import cv2 as cv
import numpy as np

from prmod.core.core_class import Rect

def calcSafeRect(roi_rect,src):
    x,y,w,h=cv.boundingRect(roi_rect)
    rows,cols=src.shape

    tl_x=np.where(x>0,x,0)
    tl_y=np.where(y>0,y,0)
    br_x=np.where(x+w<cols,x+w-1,cols-1)
    br_y=np.where(y+h<rows,y+h-1,rows-1)

    roi_width=br_x-tl_x
    roi_height=br_y-tl_y

    if roi_width<=0 or roi_height<=0:
        return False,0

    return True,Rect(tl_x,tl_y,roi_width,roi_height)

def calcSafeRect(roi_rect,width,height):
    x,y,w,h=cv.boundingRect(roi_rect)

    tl_x=np.where(x>0,x,0)
    tl_y=np.where(y>0,y,0)
    br_x=np.where(x+w<width,x+w-1,width-1)
    br_y=np.where(y+h<height,y+h-1,height-1)

    roi_width=br_x-tl_x
    roi_height=br_y-tl_y

    if roi_width<=0 or roi_height<=0:
        return False,0

    return True,Rect(tl_x,tl_y,roi_width,roi_height)
