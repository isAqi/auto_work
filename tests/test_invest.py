# -*- coding: utf-8 -*-
# @Time    : 2020/6/22/0022 22:52
# @Author  : Aqi
# @File    : test_invest.py
# @Software: PyCharm

import ddt, unittest, traceback, json
from middleware import handler
from common import requests_handler
from decimal import Decimal

# 创建一个Handler对象
handlerMid = handler.Handler()

# 获取excel的值
caseDatas = handlerMid.excel.get_data('invest')

# 获取日志对象
logger = handlerMid.logger

@ddt.ddt()
class TestInvest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info(
            "*********************************************进入投资接口测试*********************************************")
        # 投资人登录
        cls.investors_member_id = handlerMid.investors_member_id
        cls.investors_token = handlerMid.investors_token

        # 新建一个用来测试的且借款金额为3000投资项目
        setattr(handlerMid, handlerMid.loan_id, handlerMid.loan_id())
        cls.loan_id = handlerMid.loan_id
        handlerMid.audit_loan()
        # 给投资账户充值3000块钱
        handlerMid.recharge()

    def setUp(self) -> None:
        self.db = handlerMid.mysqlMid()

    def tearDown(self) -> None:
        self.db.close()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(
            "*********************************************退出投资接口测试*********************************************")

    @ddt.data(*caseDatas)
    def test_invest(self, caseData):
        method = caseData['method']
        url = handlerMid.yaml['url']['domain'] + caseData['case_url']
        expected_results = eval(caseData['case_expected'])
        data = caseData['case_data']
        headers = caseData['headers']

        if caseData['check_sql'] is not None:
            if caseData['check_sql'] == "check_amount":
                sql_count = "select count(1) before_count from invest where loan_id={}".format(self.loan_id)
                sql_amount = "SELECT leave_amount from member where id={}".format(self.member_id)
                # 查询投资前改项目在投资表中的投资记录
                before_count = self.db.query(sql_count)["before_count"]
                # 查询该投资人投资前的余额
                before_amount = self.db.query(sql_amount)
            else:
                sql = eval(caseData['check_sql'])
                self.db.query(sql)

        data = handlerMid.replace_data(data)
        headers = handlerMid.replace_data(headers)

        data = json.loads(data)
        headers = json.loads(headers)

        # 访问接口
        res = requests_handler.visit(url, method=method, json=data, headers=headers)

        try:
            actual_results = res.json()
            self.assertEqual(expected_results["code"], actual_results["code"])
            self.assertEqual(expected_results["msg"], actual_results["msg"])

            if actual_results["code"] == 0:
                sql_count = "select count(1) after_count from invest where loan_id={}".format(self.loan_id)
                sql_amount = "SELECT after_amount from member where id={}".format(self.member_id)
                # 查询投资前改项目在投资表中的投资记录
                after_count = self.db.query(sql_count)["after_count"]
                # 查询该投资人投资前的余额
                after_amount = self.db.query(sql_amount)

                # 是否在invest中生成一条记录
                self.assertEqual(before_count + 1, after_count)
                # 投资前的余额剪去投资金额等于投资后余额
                self.assertEqual(before_amount - Decimal(str(data['amount'])), after_amount)

            handlerMid.excel.update_excel('audit', caseData["case_id"] + 1, 10, 'pass')
            logger.info("第 {} 条测试用例通过".format(caseData["case_id"]))
        except Exception as e:
            handlerMid.excel.update_excel('audit', caseData["case_id"] + 1, 10, 'fail')
            logger.error("测试用例无法通过，预期结果：{}！=实际结果：{}".format(expected_results, res.json()))
            logger.error(traceback.format_exc())
            raise e

