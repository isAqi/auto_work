# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 16:20
# @Author  : Aqi
# @File    : requests_handler.py
# @Software: PyCharm

import requests
import logging
import traceback


def visit(url, method='get', params=None, data=None, json=None, **kwargs):
    try:
        res = requests.request(method, url, params=params, data=data, json=json, **kwargs)
        return res
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        raise e
