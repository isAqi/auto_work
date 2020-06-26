# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 16:28
# @Author  : Aqi
# @File    : yaml_handler.py
# @Software: PyCharm

import yaml


def get_data(yamlPath):
    with open(yamlPath, encoding='utf-8') as file:
        conf = yaml.load(file, Loader=yaml.SafeLoader)
    return conf


def write_yaml(filePath, data):
    with open(filePath, 'w', encoding='utf8') as file:
        yaml.dump(data, file)
