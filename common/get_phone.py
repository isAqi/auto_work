# -*- coding: utf-8 -*-
# @Time    : 2020/6/12/0012 9:54
# @Author  : Aqi
# @File    : get_phone.py
# @Software: PyCharm

import random
import string
from middleware import handler

# 创建一个Handler对象
handlerMid = handler.Handler()

# 返回随机生成且数据库中不存在的手机号
def random_new_phoneno():
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187',
                 '188',
                 '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']

    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 8))
    phoneNo = start + end;
    sql = "select count(1) as results from futureloan.member where mobile_phone={}".format(phoneNo)
    mysqlHandler = handlerMid.mysqlMid()
    result = mysqlHandler.query(sql)
    mysqlHandler.close()

    if result['results'] == 1:
        return random_new_phoneno()
    else:
        return phoneNo

# 返回数据库中存在的一个手机号
def old_phoneno():
    sql = "select mobile_phone from futureloan.member limit 1"
    mysqlHandler = handlerMid.mysqlMid()
    result = mysqlHandler.query(sql)
    mysqlHandler.close()
    if result['mobile_phone'] is not None:
        return result['mobile_phone']
    else:
        return None

# 检查该手机号是否在数据库中已存在
def check_phoneno(phoneno):
    sql = "select count(1) as results from futureloan.member where mobile_phone={}".format(phoneno)
    mysqlHandler = handlerMid.mysqlMid()
    result = mysqlHandler.query(sql)
    mysqlHandler.close()
    if result['results'] == 1:
        return "yes"
    else:
        return "no"