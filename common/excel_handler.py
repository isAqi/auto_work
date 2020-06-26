# -*- coding: utf-8 -*-
# @Time    : 2020/6/10/0010 16:06
# @Author  : Aqi
# @File    : excel_handler.py
# @Software: PyCharm

import openpyxl
from openpyxl import workbook
from openpyxl.worksheet import worksheet
from config import config


class ExcelHandler:

    def __init__(self, excelPath):
        self.excelPath = excelPath
        self.workbook = None

    def _open_excel(self):
        workbook = openpyxl.load_workbook(self.excelPath)
        self.workbook = workbook

    def _get_sheet(self, sheetName):
        self._open_excel()
        sheet: worksheet = self.workbook[sheetName]
        return sheet

    def get_data(self, sheetName):
        sheet: worksheet = self._get_sheet(sheetName)
        rows = list(sheet.rows)

        list_data = []
        for row in rows[1:]:
            dict_data = {}
            for i, cell in enumerate(row):
                dict_data[rows[0][i].value] = cell.value
            list_data.append(dict_data)
        return list_data

    def update_excel(self, sheetName, row, clo, data):
        sheet = self._get_sheet(sheetName)
        sheet.cell(row, clo, data)
        self._save_excel()

    def _save_excel(self):
        self.workbook.save(self.excelPath)
        self.close_excel()

    def close_excel(self):
        workbook.Workbook.close(self)

if __name__ == '__main__':
    ExcelHandler(config.DATA_PATH).update_excel('注册', 2, 9, 'pass')
