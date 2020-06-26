# -*- coding: utf-8 -*-
# @Time    : 2020/6/7/0007 22:29
# @Author  : Aqi
# @File    : logger_enc.py
# @Software: PyCharm

import logging

class LoggerHander(logging.Logger):

    def __init__(self, name, level=logging.DEBUG):
        self.name = name
        self.level = level
        super(LoggerHander, self).__init__(name=name, level=level)

    def in_strem(self, level=logging.DEBUG, fmt=None):
        StreamHandler = logging.StreamHandler()
        StreamHandler.setLevel(level)
        fmt = logging.Formatter(fmt)
        StreamHandler.setFormatter(fmt)
        self.addHandler(StreamHandler)

    def in_file(self, fileName, model='a', level=logging.DEBUG, fmt=None):
        FileHandler = logging.FileHandler(fileName, mode=model, encoding='utf-8')
        FileHandler.setLevel(level)
        fmt = logging.Formatter(fmt)
        FileHandler.setFormatter(fmt)
        self.addHandler(FileHandler)
