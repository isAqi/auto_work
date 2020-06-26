# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 14:33
# @Author  : Aqi
# @File    : run.py
# @Software: PyCharm

import unittest
from HtmlTestRunner import HTMLTestRunner
from config import config
import os


load = unittest.TestLoader()
suit = load.discover(config.CASE_PATH)

if not os.path.exists(config.REPORTS_DIR_PATH):
    os.makedirs(config.REPORTS_DIR_PATH)

with open(config.REPORTS_FILE_PATH, 'wb') as file:
    runner = HTMLTestRunner(file, 2, title="aqi", description='unittest')
    runner.run(suit)

if __name__ == '__main__':
    unittest.main()
