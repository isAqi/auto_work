# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 14:34
# @Author  : Aqi
# @File    : test_register.py
# @Software: PyCharm

import unittest, ddt, json, traceback
from middleware import handler
from common import requests_handler, get_phone


# 创建一个Handler对象
handlerMid = handler.Handler()

# 获取excel的值
CaseDatas = handlerMid.excel.get_data('login')

# 获取日志对象
logger = handlerMid.logger

@ddt.ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info(
            "*********************************************进入登录接口测试*********************************************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(
            "*********************************************退出登录接口测试*********************************************")

    @ddt.data(*CaseDatas)
    def test_login(self, caseInfo):
        method = caseInfo['method']
        url = handlerMid.yaml['url']['domain'] + caseInfo['case_url']
        data = json.loads(caseInfo['case_data'])
        headers = json.loads(caseInfo['headers'])
        expected_results = eval(caseInfo['case_expected'])

        # 设置登录成功用例的账号和密码
        if data['mobile_phone'] == "#login_phone#" and data['pwd'] == "#pwd#":
            data["mobile_phone"] = handlerMid.yaml["login_success"]["mobile_phone"]
            data["pwd"] = handlerMid.yaml["login_success"]["pwd"]

        # 登录失败手机号未注册（random_new_phoneno（）随机数获取电话号码）
        if data['mobile_phone'] == "#newPhone#":
            data["mobile_phone"] = data["mobile_phone"].replace("#newPhone", get_phone.random_new_phoneno())
        # 登录失败密码为空或错误 （old_phoneno（）从数据库中查找一个存在的电话号码）
        if data['mobile_phone'] == "#oldPhone#":
            data["mobile_phone"] = data["mobile_phone"].replace("#oldPhone", get_phone.old_phoneno())

        # 访问接口
        res = requests_handler.visit(url, method=method, json=data, headers=headers)

        try:
            for key, value in expected_results.items():
                self.assertEqual(value, res.json()[key])
            logger.info("第 {} 条测试用例通过".format(caseInfo["case_id"]))
            handlerMid.excel.update_excel('login', caseInfo["case_id"] + 1, 9, 'pass')
        except AssertionError as e:
            handlerMid.excel.update_excel('login', caseInfo["case_id"] + 1, 9, 'fail')
            logger.error("测试用例无法通过，预期结果：{}！=实际结果：{}".format(expected_results, res.json()))
            logger.error(traceback.format_exc())
            raise e


if __name__ == '__main__':
    unittest.main()
