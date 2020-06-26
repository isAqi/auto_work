# -*- coding: utf-8 -*-
# @Time    : 2020/6/17/0017 9:58
# @Author  : Aqi
# @File    : test_recharge.py
# @Software: PyCharm

import unittest, ddt, traceback, json
from middleware import handler
from common import requests_handler

# 创建一个Handler对象
handlerMid = handler.Handler()

# 获取excel的值
caseDatas = handlerMid.excel.get_data('addProject')

# 获取日志对象
logger = handlerMid.logger


@ddt.ddt()
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info(
            "*********************************************进入新增项目接口测试*********************************************")
        cls.token = handlerMid.token
        cls.member_id = handlerMid.member_id

    def setUp(self) -> None:
        self.db = handlerMid.mysqlMid()

    def tearDown(self) -> None:
        self.db.close()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(
            "*********************************************退出新增项目接口测试*********************************************")

    @ddt.data(*caseDatas)
    def test_recharge(self, caseData):
        method = caseData['method']
        url = handlerMid.yaml['url']['domain'] + caseData['case_url']
        data = caseData['case_data']
        headers = json.loads(caseData['headers'])
        expected_results = eval(caseData['case_expected'])

        # 使用已经登录的memberId 更换用例数据中member_id的值
        # if '#memberId' in data:
        #     data = data.replace("#memberId", str(self.member_id))
        #     # data["member_id"] = self.member_id

        # data = json.loads(data)

        # 使用已经登录的token 更换用例数据中token的值
        # if '#Token' in headers["Authorization"]:
        #     headers["Authorization"] = self.token

        data = handlerMid.replace_data(caseData['case_data'])
        headers = handlerMid.replace_data(caseData['headers'])
        headers = json.loads(headers)
        data = json.loads(data)


        # 查询新增项目前数据库中 该用户的项目数
        if caseData['check_sql'] is not None:
            before_sql = "SELECT COUNT(1) before_count FROM loan WHERE member_id={}".format(self.member_id)
            before_count = self.db.query(before_sql, one=False)[0]['before_count']

        # 访问接口
        res = requests_handler.visit(url, method=method, json=data, headers=headers)

        try:
            for key, value in expected_results.items():
                self.assertEqual(value, res.json()[key])

            # 查询新增项目后数据库中 该用户的
            # 项目数
            if res.json()["code"] == 0:
                after_sql = "SELECT COUNT(1) after_count FROM loan WHERE member_id={}".format(self.member_id)
                after_count = self.db.query(after_sql, one=False)[0]['after_count']
                # 新增前后项目数
                self.assertEqual(before_count + 1, after_count)
            handlerMid.excel.update_excel('addProject', caseData["case_id"] + 1, 10, 'pass')
            logger.info("第 {} 条测试用例通过".format(caseData["case_id"]))
        except Exception as e:
            handlerMid.excel.update_excel('addProject', caseData["case_id"] + 1, 10, 'fail')
            logger.error("测试用例无法通过，预期结果：{}！=实际结果：{}".format(expected_results, res.json()))
            logger.error(traceback.format_exc())
            raise e


if __name__ == '__main__':
    unittest.main()
