# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:CPlateLocate.py
@time:2018/8/8 11:15
"""

import cv2 as cv
import numpy as np

from prmod.config import Color
from test.core_func import calcSafeRect


class CPlateLocate:
    DEFAULT_GAUSSIANBLUR_SIZE = 5
    SOBEL_SCALE = 1
    SOBEL_DELTA = 0
    SOBEL_DDEPTH = cv.CV_16S
    SOBEL_X_WEIGHT = 1
    SOBEL_Y_WEIGHT = 0
    DEFAULT_MORPH_SIZE_WIDTH = 17
    DEFAULT_MORPH_SIZE_HEIGHT = 3

    WIDTH = 136
    HEIGHT = 36
    TYPE = cv.CV_8UC3

    DEFAULT_ERROR = 0.9
    DEFAULT_ASPECT = 3.75
    DEFAULT_VERIFY_MIN = 2
    DEFAULT_VERIFY_MAX = 24

    DEFAULT_ANGLE = 60

    DEFAULT_DEBUG = False

    def __init__(self):
        # 高斯模糊所用变量
        self.__GaussianBlurSize = CPlateLocate.DEFAULT_GAUSSIANBLUR_SIZE

        # 连接操作所用变量
        self.__MorphSizeWidth = CPlateLocate.DEFAULT_MORPH_SIZE_WIDTH
        self.__MorphSizeHeight = CPlateLocate.DEFAULT_MORPH_SIZE_HEIGHT

        # verifySize所用变量
        self.__error = CPlateLocate.DEFAULT_ERROR
        self.__aspect = CPlateLocate.DEFAULT_ASPECT
        self.__verifyMin = CPlateLocate.DEFAULT_VERIFY_MIN
        self.__verifyMax = CPlateLocate.DEFAULT_VERIFY_MAX

        # 角度判断所用变量
        self.__angle = CPlateLocate.DEFAULT_ANGLE

        # 是否开启调试模式，0关闭，非0开启
        self.__debug = CPlateLocate.DEFAULT_DEBUG

    def verifySizes(self, mr):

        error = self.__error

        """
        China car plate size: 440mm*140mm，aspect 3.142857
        Real car plate size: 136 * 32, aspect 4
        """
        aspect = self.__aspect

        min = self.__verifyMin * 34 * 8
        max = self.__verifyMax * 34 * 8

        rmin = aspect - aspect * error
        rmax = aspect + aspect * error

        width = mr[1][0]
        height = mr[1][1]

        if width == 0 or height == 0:
            return False

        area = width * height
        r = width / height

        if r < 1:
            r = height / width

        if area < min or area > max or r < rmin or r > rmax:
            return False
        else:
            return True

    def setLifemode(self, param):
        if param == True:
            self.setGaussianBlurSize(5)
            self.setMorphSizeWidth(10)
            self.setMorphSizeHeight(3)
            self.setVerifyError(0.75)
            self.setVerifyAspect(4.0)
            self.setVerifyMin(1)
            self.setVerifyMiax(200)
        else:
            self.setGaussianBlurSize(CPlateLocate.DEFAULT_GAUSSIANBLUR_SIZE)
            self.setMorphSizeWidth(CPlateLocate.DEFAULT_MORPH_SIZE_WIDTH)
            self.setMorphSizeHeight(CPlateLocate.DEFAULT_MORPH_SIZE_HEIGHT)
            self.setVerifyError(CPlateLocate.DEFAULT_ERROR)
            self.setVerifyAspect(CPlateLocate.DEFAULT_ASPECT)
            self.setVerifyMin(CPlateLocate.DEFAULT_VERIFY_MIN)
            self.setVerifyMiax(CPlateLocate.DEFAULT_VERIFY_MAX)

    def plateLocate(self, src, index):
        pass

    def plateColorLocate(self, src):
        src_clone = np.copy(src)

        src_b_blue, rects_color_blue = self.colorSearch(src, Color.BLUE)

        pass

    def colorSearch(self, src, color):
        outRects = []
        out=0



        return out,outRects

    def plateSobelLocateOld(self,src):
        """
        定位车牌图像
        :param src:原始图像
        :return:
            resultList 一个numpy.ndarray的list，存储所有抓取到的图像
            成功返回0，否则返回-1
        """
        resultList = []
        debugList = []

        scale = CPlateLocate.SOBEL_SCALE
        delta = CPlateLocate.SOBEL_DELTA
        ddepth = CPlateLocate.SOBEL_DDEPTH

        if type(src) == None:
            return -1, resultList, debugList

        # 高斯模糊。第二个参数中的数字影响车牌定位的效果。
        src_blur = cv.GaussianBlur(src, (self.__GaussianBlurSize, self.__GaussianBlurSize), 0, 0, cv.BORDER_DEFAULT)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_src_blur.jpg", src_blur)
            debugList.append(src_blur)

        # 将其转换为灰度图
        src_gray = cv.cvtColor(src_blur, cv.COLOR_BGR2GRAY)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_src_gray.jpg", src_gray)
            debugList.append(src_gray)

        grad_x = cv.Sobel(src_gray, ddepth, 1, 0, 3, 1, scale, delta, cv.BORDER_DEFAULT)
        abs_grad_x = cv.convertScaleAbs(grad_x)

        grad_y = cv.Sobel(src_gray, ddepth, 0, 1, 3, 1, scale, delta, cv.BORDER_DEFAULT)
        abs_grad_y = cv.convertScaleAbs(grad_y)

        grad = cv.addWeighted(abs_grad_x, CPlateLocate.SOBEL_X_WEIGHT, abs_grad_y, CPlateLocate.SOBEL_Y_WEIGHT, 0)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_grad.jpg", grad)
            debugList.append(grad)

        img_threshold = cv.threshold(grad, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY)[1]

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_img_threshold.jpg", img_threshold)
            debugList.append(img_threshold)

        element = cv.getStructuringElement(cv.MORPH_RECT, (self.__MorphSizeWidth, self.__MorphSizeHeight))
        img_threshold_close = cv.morphologyEx(img_threshold, cv.MORPH_CLOSE, element)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_img_threshold_close.jpg", img_threshold_close)
            debugList.append(img_threshold_close)

        contours = cv.findContours(img_threshold_close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]

        if self.__debug:
            result = src.copy()
            drawContoursResult = cv.drawContours(result, contours, -1, (0, 0, 255), 1)
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_drawContoursResult.jpg", drawContoursResult)
            debugList.append(drawContoursResult)

        if self.__debug:
            rect_img = result.copy()
            debugList.append(rect_img)

        k = 0
        for i in range(len(contours)):
            mr = cv.minAreaRect(contours[i])
            if self.verifySizes(mr):

                width = mr[1][0]
                height = mr[1][1]
                r = width / height
                angle = mr[2]
                center = (mr[0][0] + width / 2, mr[0][1] + height / 2)
                if r < 1:
                    angle = 90 + angle
                    width, height = height, width
                if angle - self.__angle < 0 and angle + self.__angle > 0:
                    rotmat = cv.getRotationMatrix2D(center, angle, 1)
                    rows, cols = src.shape[0], src.shape[1]
                    img_rotated = cv.warpAffine(src, rotmat, (rows, cols), cv.INTER_CUBIC)
                    k += 1
                    resultMat = self.showResultMat(img_rotated, (int(width), int(height)), mr[0], k)
                    resultList.append(resultMat)

                    if self.__debug:
                        rect_points = cv.boxPoints(mr)
                        rect_points = np.int0(rect_points)
                        rect_img = cv.drawContours(rect_img, [rect_points], -1, (0, 255, 255), 1)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_rect_img.jpg", rect_img)

        return 0, resultList, debugList

    def plateSobelLocate(self,src):

        rows,cols = src.shape

        bound_rects_part=[]

        bound_rects=self.sobelFrtSearch(src)

        for i in range(len(bound_rects)):
            fRatio=(bound_rects[i].x*1.0)/bound_rects[i].y

            if fRatio<3.0 and fRatio>1.0 and bound_rects[i].height<120:
                itemRect=bound_rects[i]

                itemRect.x=itemRect.x=itemRect.height*(4-fRatio)

                if itemRect.x<0:
                    itemRect.x=0

                itemRect.width=itemRect.width+itemRect.height*2*(4-fRatio)

                if itemRect.width+itemRect.x>cols:
                    itemRect.width=cols-itemRect.x

                itemRect.y=itemRect.y-itemRect.height*0.08
                itemRect.height=itemRect.height*1.16

                bound_rects_part.append(itemRect)

        for i in range(len(bound_rects_part)):
            bound_rect=bound_rects_part[i]
            refpoint=bound_rect.getPoint()

            x=np.where(bound_rect.x>0,bound_rect.x,0)
            y=np.where(bound_rect.y>0,bound_rect.y,0)
            width=np.where(x+bound_rect.width<cols,bound_rect.width,cols-x)
            height=np.where(y+bound_rect.height<rows,bound_rect.height,rows-y)

            bound_mat=src[y:height,x:width]



        pass

    def sobelFrtSearch(self,src):

        src_threshold=self.sobelFrtSearch(src,self.__GaussianBlurSize,self.__MorphSizeWidth,self.__MorphSizeHeight)

        contours = cv.findContours(src_threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]

        first_rects=[]

        for i in range(len(contours)):
            mr = cv.minAreaRect(contours[i])

            if self.verifySizes(mr):
                first_rects.append(contours[i])

        outRect=[]

        for i in range(len(first_rects)):
            roi_rect=first_rects[i]

            isok,safeBoundRect=calcSafeRect(roi_rect,src)
            if isok:
                outRect.append(safeBoundRect)

        return outRect

    def sobelSecSearchPart(self,src):
        bound_threshold=self.sobelOper(src,3,6,2)

        temBoundThread=np.copy(bound_threshold)



        pass

    def sobelOper(self,src,blurSize,morphW,morphH):
        mat_blur=np.copy(src)
        mat_blur=cv.GaussianBlur(mat_blur,(blurSize,blurSize),0,0,cv.BORDER_DEFAULT)

        if len(mat_blur.shape)==3:
            mat_gray=cv.cvtColor(mat_blur,cv.COLOR_RGB2GRAY)
        else:
            mat_gray=mat_blur

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_sobelOper_gray.jpg", mat_gray)

        scale=self.SOBEL_SCALE
        delta=self.SOBEL_DELTA
        ddepth=self.SOBEL_DDEPTH

        grad_x = cv.Sobel(mat_gray, ddepth, 1, 0, 3, 1, scale, delta, cv.BORDER_DEFAULT)
        abs_grad_x = cv.convertScaleAbs(grad_x)

        grad = cv.addWeighted(abs_grad_x, CPlateLocate.SOBEL_X_WEIGHT, 0, 0, 0)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_sobelOper_grad.jpg", grad)

        otsu_thresh_val,mat_threshold = cv.threshold(grad, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_sobelOper_grayBINARY.jpg", mat_threshold)

        element = cv.getStructuringElement(cv.MORPH_RECT, (morphW,morphH))
        mat_threshold = cv.morphologyEx(mat_threshold, cv.MORPH_CLOSE, element)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_sobelOper_phologyEx.jpg", mat_threshold)

        return mat_threshold


    def showResultMat(self, src, rect_size, point, index):

        img_crop = cv.getRectSubPix(src, rect_size, point)

        resultResized = cv.resize(img_crop, (CPlateLocate.WIDTH, CPlateLocate.HEIGHT), cv.INTER_CUBIC)

        if self.__debug:
            cv.imwrite("resources/image/tmp/CPlateLocate_plateLocate_resultResized" + str(index) + ".jpg", resultResized)

        return resultResized

    def setGaussianBlurSize(self, param):
        self.__GaussianBlurSize = param

    def getGaussianBlurSize(self):
        return self.__GaussianBlurSize

    def setMorphSizeWidth(self, param):
        self.__MorphSizeWidth = param

    def getMorphSizeWidth(self, param):
        return self.__MorphSizeWidth

    def setMorphSizeHeight(self, param):
        self.__MorphSizeHeight = param

    def getMorphSizeHeight(self, param):
        return self.__MorphSizeHeight

    def setVerifyError(self, param):
        self.__error = param

    def getVerifyError(self):
        return self.__error

    def setVerifyAspect(self, param):
        self.__aspect = param

    def getVerifyAspect(self):
        return self.__aspect

    def setVerifyMin(self, param):
        self.__verifyMin = param

    def setVerifyMiax(self, param):
        self.__verifyMax = param

    def setJudgeAngle(self, param):
        self.__angle = param

    def setDebug(self, param):
        self.__debug = param

    def getDebug(self):
        return self.__debug
