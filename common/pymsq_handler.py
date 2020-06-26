# -*- coding: utf-8 -*-
# @Time    : 2020/6/11/0011 21:42
# @Author  : Aqi
# @File    : pymsq_handler.py
# @Software: PyCharm

import pymysql
from pymysql.cursors import DictCursor

class MysqlHandler():

    def __init__(self, host=None, database=None, port=None, user=None, password=None, charset=None):
        self.conn = pymysql.connect(
            host=host,
            database=database,
            port=port,
            user=user,
            password=password,
            charset=charset,
            cursorclass=DictCursor
        )
        self.cursor = self.conn.cursor()


    def query(self, sql, one=True):
        # 最新的数据更新，提交事务
        self.conn.commit()
        self.cursor.execute(sql)
        if one:
            return self.cursor.fetchone()
        return self.cursor.fetchall()


    def close(self):
        self.cursor.close()
        self.conn.close()
