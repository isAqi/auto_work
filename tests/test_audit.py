# -*- coding: utf-8 -*-
# @Time    : 2020/6/19/0019 21:46
# @Author  : Aqi
# @File    : test_audit.py
# @Software: PyCharm

import unittest, ddt, traceback, json
from middleware import handler
from common import requests_handler

# 创建一个Handler对象
handlerMid = handler.Handler()

# 获取excel的值
caseDatas = handlerMid.excel.get_data('audit')

# 获取日志对象
logger = handlerMid.logger

@ddt.ddt()
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info(
            "*********************************************进入新增项目接口测试*********************************************")
        # 普通用户登录
        cls.token = handlerMid.token
        cls.member_id = handlerMid.member_id

        # 管理员登录
        cls.admin_token = handlerMid.admin_token

    def setUp(self) -> None:
        self.db = handlerMid.mysqlMid()

        setattr(handlerMid, handlerMid.loan_id, handlerMid.loan_id())
        self.loan_id = handlerMid.loan_id

    def tearDown(self) -> None:
        self.db.close()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(
            "*********************************************退出新增项目接口测试*********************************************")

    @ddt.data(*caseDatas)
    def test_audit(self, caseData):
        method = caseData['method']
        url = handlerMid.yaml['url']['domain'] + caseData['case_url']
        data = caseData['case_data']
        # headers = json.loads(caseData['headers'])
        expected_results = eval(caseData['case_expected'])

        # 替换项目id
        # if "#loanId" in data:
        #     data = data.replace("#loanId", str(self.loan_id))

        # 替换一个不在审核状态当中的项目id
        if "passLoanId" in data:
            sql = "SELECT id FROM loan WHERE status != 1;"
            loan = self.db.query(sql)['id']
            data = data.replace("#passLoanId", str(loan))
            # data = data.replace("#loanId", str(handlerMid.pass_loan_id))

        data = handlerMid.replace_data(data)
        headers = handlerMid.replace_data(caseData['headers'])

        headers = json.loads(headers)
        data = eval(data)

        # # 使用管理员登录的token 更换用例数据中token的值
        # if '#AdminToken' in headers["Authorization"]:
        #     headers["Authorization"] = self.admin_token
        #
        # # 普通用户审核
        # if '#Token' in headers["Authorization"]:
        #     headers["Authorization"] = self.token

        # 访问接口
        res = requests_handler.visit(url, method=method, json=data, headers=headers)

        try:

            actual_results = res.json()
            self.assertEqual(expected_results["code"], actual_results["code"])
            self.assertEqual(expected_results["msg"], actual_results["msg"])

            # 查询审核项目后数据库中 该项目的状态
            if actual_results["code"] == 0:
                sql = "SELECT * FROM loan WHERE id={}".format(self.loan_id)
                actual_status = self.db.query(sql)['status']
                # 新增前后项目数
                self.assertEqual(expected_results["status"], actual_status)

                # handlerMid.pass_loan_id = actual_status["id"]

            handlerMid.excel.update_excel('audit', caseData["case_id"] + 1, 10, 'pass')
            logger.info("第 {} 条测试用例通过".format(caseData["case_id"]))
        except Exception as e:
            handlerMid.excel.update_excel('audit', caseData["case_id"] + 1, 10, 'fail')
            logger.error("测试用例无法通过，预期结果：{}！=实际结果：{}".format(expected_results, res.json()))
            logger.error(traceback.format_exc())
            raise e


if __name__ == '__main__':
    unittest.main()


