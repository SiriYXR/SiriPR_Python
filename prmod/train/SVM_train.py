# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:SVM_train.py
@time:2018/10/3 16:32
"""

from siripyd.siripr import SvmTrain

class SVMTrain():

    def __init__(self):
        self.plates_folder=''
        self.xml=''

    def train(self):
        svmtrain=SvmTrain(self.plates_folder,self.xml)
        svmtrain.train()

    def setPlatesFolder(self,path):
        self.plates_folder=path

    def setXML(self,path):
        self.xml=path

if __name__ == "__main__":
    test=SVMTrain()
    test.setPlatesFolder('./train/SVM')
    test.setXML('./train/SVM')
    test.train()