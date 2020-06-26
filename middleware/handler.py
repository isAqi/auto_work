# -*- coding: utf-8 -*-
# @Time    : 2020/6/13/0013 10:27
# @Author  : Aqi
# @File    : handler.py
# @Software: PyCharm

import os, jsonpath
from config import config
from common import yaml_handler, excel_handler, logger_enc, requests_handler
from common.pymsq_handler import MysqlHandler


class MsqlHandlerMid(MysqlHandler):

    def __init__(self):
        dbData = Handler.yaml['db']
        super().__init__(
            host=dbData['host'],
            database=dbData['database'],
            port=dbData['port'],
            user=dbData['user'],
            password=dbData['password'],
            charset=dbData['charset']
        )


class Handler:
    """
     初始化所有的数据，
     在其他的模块当中重复使用，
     是从common中实例化对象
    """

    # 加载 python 配置项
    conf = config

    # YAML数据
    yaml = yaml_handler.get_data(config.YAML_PATH)

    # excel数据
    excel = excel_handler.ExcelHandler(config.DATA_PATH)

    loan_id = None

    # logger
    __logger_config = yaml['log']
    logger = logger_enc.LoggerHander(__logger_config['name'], level=__logger_config['logger_level'])
    logger.in_strem(level=__logger_config['stream_level'],
                    fmt='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    logger.in_file(os.path.join(config.LOG_PATH, __logger_config['filePath']), level=__logger_config['stream_level'],
                   fmt='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')

    mysqlMid = MsqlHandlerMid

    # 普通用户
    @property
    def token(self):
        return self.login("login_success")["token"]

    @property
    def member_id(self):
        return self.login("login_success")["member_id"]

    # 投资人
    @property
    def investors_token(self):
        return self.login("login_success")["token"]

    @property
    def investors_member_id(self):
        return self.login("login_investors")["member_id"]

    # 会员
    @property
    def admin_token(self):
        return self.login("login_investors")["token"]

    def loan_id(self,da):
        return self.add_loan()

    # 登录
    def login(self, user):
        res = requests_handler.visit(
            Handler.yaml['url']['domain'] + "/member/login",
            method='post',
            headers={"X-Lemonban-Media-Type": "lemonban.v2"},
            json=Handler.yaml[user]
        )
        data = res.json()

        token_str = jsonpath.jsonpath(data, "$..token")[0]
        token_type = jsonpath.jsonpath(data, "$..token_type")[0]
        token = " ".join([token_type, token_str])
        member_id = jsonpath.jsonpath(data, "$..id")[0]
        return {"token": token, "member_id": member_id}

    def replace_data(self, data):
        import re
        # 表达式 .* 就是单个字符匹配任意bai次，即贪婪匹配。 表达式du .*? 是满足zhi条件的情况只匹配一次，即最小dao匹配
        patten = r"#(.*?)#"
        while re.search(patten, data):
            key = re.search(patten, data).group(1)
            value = getattr(self, key, "")
            # count 表示匹配到的第一个 字符串完成替换
            data = re.sub(patten, str(value), data, count=1)
        return data

    # 添加项目
    def add_loan(self):
        data = {
            "member_id": self.member_id,
            "title": "一个测试项目",
            "amount": 3000,
            "loan_rate": 20.0,
            "loan_term": 6,
            "loan_date_type": 1,
            "bidding_days": 5
        }

        res = requests_handler.visit(
            Handler.yaml['url']['domain'] + "/loan/add",
            method='post',
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data
        )

        result_data = res.json()

        loan_id = jsonpath.jsonpath(result_data, "$..id")[0]

        return loan_id

    # 审核项目
    def audit_loan(self):
        data = {
              "loan_id": self.loan_id,
              "approved_or_not": True
        }

        res = requests_handler.visit(
            Handler.yaml['url']['domain'] + "/loan/audit",
            method='patch',
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.admin_token},
            json=data
        )

    # 充值
    def recharge(self):
        data = {
            "member_id": self.investors_member_id,
            "amount": "3000"
        }

        res = requests_handler.visit(
            Handler.yaml['url']['domain'] + "/member/recharge",
            method='post',
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.investors_token},
            json=data
        )
