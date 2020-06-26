# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 14:38
# @Author  : Aqi
# @File    : config.py
# @Software: PyCharm
import os
from datetime import datetime
from common import yaml_handler

# 设置一个登录成功的账号

# 项目地址
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# yaml文件路径
YAML_PATH = os.path.join(BASE_PATH, 'config', 'config.yaml')

# yaml文件的值
YAML_DATA = yaml_handler.get_data(YAML_PATH)

# 测试用例路径
CASE_PATH = os.path.join(BASE_PATH, 'tests')

# 测试报告地址
REPORTS_PATH = os.path.join(BASE_PATH, 'reports')
REPORTS_DIR_PATH = os.path.join(REPORTS_PATH, datetime.now().strftime('%Y-%m-%d-%H'))
FILE_NAME = os.path.join(REPORTS_DIR_PATH, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
REPORTS_FILE_PATH = os.path.join(REPORTS_DIR_PATH, FILE_NAME + '.html')

# 测试数据路径
DATA_PATH = os.path.join(BASE_PATH, 'data', YAML_DATA['excel']['file'])


# LOG 数据路径
LOG_PATH = os.path.join(BASE_PATH, "logs")

