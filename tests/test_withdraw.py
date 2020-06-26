# -*- coding: utf-8 -*-
# @Time    : 2020/6/17/0017 9:58
# @Author  : Aqi
# @File    : test_recharge.py
# @Software: PyCharm

import unittest, ddt, traceback, json
from middleware import handler
from common import requests_handler
from decimal import Decimal

# 创建一个Handler对象
handlerMid = handler.Handler()

# 获取excel的值
caseDatas = handlerMid.excel.get_data('withdraw')

# 获取日志对象
logger = handlerMid.logger

@ddt.ddt
class TestWithdraw(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info(
            "*********************************************进入提现接口测试*********************************************")
        cls.token = handlerMid.token
        cls.member_id = handlerMid.member_id

    def setUp(self) -> None:
        self.db = handlerMid.mysqlMid()

    def tearDown(self) -> None:
        self.db.close()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(
            "*********************************************退出提现接口测试*********************************************")

    @ddt.data(*caseDatas)
    def test_withdraw(self, caseData):
        method = caseData['method']
        url = handlerMid.yaml['url']['domain'] + caseData['case_url']

        expected_results = eval(caseData['case_expected'])

        # # 使用已经登录的memberId 更换用例数据中member_id的值
        # if data['member_id'] == '#memberId':
        #     # data = data.replace("#menberId", self.member_id)
        #     data["member_id"] = self.member_id
        #
        # # 使用已经登录的token 更换用例数据中token的值
        # if headers["Authorization"] == '#Token':
        #     headers["Authorization"] = self.token

        data = handlerMid.replace_data(caseData['case_data'])
        headers = handlerMid.replace_data(caseData['headers'])
        headers = json.loads(headers)
        data = json.loads(data)


        # 查询是否需要更新数据
        if caseData['check_sql'] == "update_select_amount1":
            update_amount_sql = "UPDATE member SET leave_amount=500000 where id={}".format(self.member_id)
            self.db.query(update_amount_sql)

        if caseData['check_sql'] == "update_select_amount2":
            update_amount_sql = "UPDATE member SET leave_amount=499999.99 where id={}".format(self.member_id)
            self.db.query(update_amount_sql)

        if caseData['check_sql'] is not None:
            # log_sql = "SELECT * from loan where member_id={}".format(self.member_id)
            # before_loan = self.db.query(log_sql, one=False)['leave_amount']
            before_sql = "SELECT leave_amount from member where id={}".format(self.member_id)
            before_amount = self.db.query(before_sql)['leave_amount']

        # 访问接口
        res = requests_handler.visit(url, method=method, json=data, headers=headers)

        try:
            for key, value in expected_results.items():
                self.assertEqual(value, res.json()[key])

            # 提现成功后需要判断数据库中的金额是否正确
            if res.json()["code"] == 0:
                after_sql = "SELECT leave_amount from member where id={}".format(self.member_id)
                after_amount = self.db.query(after_sql)['leave_amount']
                # 断言充值金额加上充值前的金额 要等于 充值成功后的金额
                self.assertEqual(before_amount - Decimal(str(data['amount'])), after_amount)
                logger.info("第 {} 条测试用例通过 提现前金额：{} - 提现金额：{} - 提现后金额：{}".format(caseData["case_id"], before_amount, Decimal(str(data['amount'])), after_amount))

            handlerMid.excel.update_excel('recharge', caseData["case_id"] + 1, 10, 'pass')
            logger.info("第 {} 条测试用例通过".format(caseData["case_id"]))
        except Exception as e:
            handlerMid.excel.update_excel('recharge', caseData["case_id"] + 1, 10, 'fail')
            logger.error("测试用例无法通过，预期结果：{}！=实际结果：{}".format(expected_results, res.json()))
            logger.error(traceback.format_exc())
            raise e


if __name__ == '__main__':
    unittest.main()