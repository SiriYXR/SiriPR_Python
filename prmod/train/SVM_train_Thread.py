# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:SVM_train_Thread.py
@time:2018/10/5 10:59
"""
import threading

from prmod.train.SVM_train import SVMTrain


class SVM_train_Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(SVM_train_Thread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True



    def run(self):
        while self.__running.isSet():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            test = SVMTrain()
            test.setPlatesFolder('resources/train/SVM')
            test.setXML('resources/train/svm.xml')
            test.train()

            self.stop()


    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如果已经暂停的话
        self.__running.clear()  # 设置为False