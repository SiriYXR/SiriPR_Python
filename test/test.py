# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:test.py
@time:2018/8/1 14:15
"""

from test.cv_imread import cv_imread

from siripyd import siripr


img = cv_imread('E:/Coder/Python/Workspace/SiriPR/test1.jpg', 1)

# pl = CPlateLocate()
# pl.setDebug(True)
# _,result, debug = pl.plateSobelLocateOld(img)
#
# for i in result:
#     cv.imshow('result', i)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#
# for i in debug:
#     i = cv.resize(i, (1024, 720), interpolation=cv.INTER_CUBIC)
#     cv.imshow('debug', i)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

print(siripr.ImgRecognize(img,0))
