# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 14:34
# @Author  : Aqi
# @File    : test_register.py
# @Software: PyCharm

import unittest, ddt
from middleware import handler
from common import requests_handler, get_phone
import traceback
import json

# 创建一个Handler对象
handlerMid = handler.Handler()

# 获取excel的值
CaseDatas = handlerMid.excel.get_data('register')

# 获取日志对象
logger = handlerMid.logger


@ddt.ddt
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("*********************************************进入注册接口测试*********************************************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("*********************************************退出注册接口测试*********************************************")

    @ddt.data(*CaseDatas)
    def test_register(self, caseInfo):
        method = caseInfo['method']
        url = handlerMid.yaml['url']['domain'] + caseInfo['case_url']
        data = json.loads(caseInfo['case_data'])
        headers = json.loads(caseInfo['headers'])
        expected_results = eval(caseInfo['case_expected'])

        # 注册成功的用例（random_new_phoneno（）随机数获取电话号码）
        if data['mobile_phone'] == "#newPhone#":
            data["mobile_phone"] = data["mobile_phone"].replace("#newPhone", get_phone.random_new_phoneno())
        # 注册重复的用例（random_old_phoneno（）从数据库中查找一个存在的电话号码）
        if data['mobile_phone'] == "#oldPhone#":
            data["mobile_phone"] = data["mobile_phone"].replace("#oldPhone", get_phone.old_phoneno())

        # 访问接口
        res = requests_handler.visit(url, method=method, json=data, headers=headers)

        try:
            for key, value in expected_results.items():
                self.assertEqual(value, res.json()[key])

            # 注册成功 后 查看是否在数据库中存在
            if res.json()["code"] == 0:
                check_data = get_phone.check_phoneno(data["mobile_phone"])
                self.assertEqual(check_data, "yes")
            handlerMid.excel.update_excel('register', caseInfo["case_id"] + 1, 9, 'pass')
            logger.info("第 {} 条测试用例通过".format(caseInfo["case_id"]))
        except AssertionError as e:
            handlerMid.excel.update_excel('register', caseInfo["case_id"] + 1, 9, 'fail')
            logger.error("测试用例无法通过，预期结果：{}！=实际结果：{}".format(expected_results, res.json()))
            logger.error(traceback.format_exc())
            raise e


if __name__ == '__main__':
    unittest.main()