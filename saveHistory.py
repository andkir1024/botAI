import os
from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from managerQR import managerQR
from okDeskUtils import okDesk
from processorMenu import *
from aiogram.types import InputFile

import pandas as pd
from openpyxl import Workbook, load_workbook

class history:
    def __init__(self):
        pass
    def save(userInfo, msg: types.Message):
        supportMode = userInfo.supportMode.lower()
        info = msg.text
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirHistory = dir_path + mainConst.DIR_HISTORY
        if not os.path.isdir(dirHistory):
            os.mkdir(dirHistory)

        now = datetime.now() 
        current_time = now.strftime("%Y:%d:%m:%H:%M:%S")
        
        xlName = dirHistory + 'example.xlsx'
        
        wb = load_workbook(xlName)
        sheet = wb.get_sheet_by_name('sheet1')
        c = sheet['A1'].value
        new_row = ['column1', 'column2', 'column3']
        sheet.append(new_row)
        wb.save(xlName)
        return
        
        # workbook = load_workbook(filename="sample.xlsx")
        # workbook.sheetnames
        # ['Sheet 1']
        
        xl = pd.ExcelFile(xlName)
        df1 = xl.parse(xl.sheet_names)
        
        list1 = [10, 20, 30, 40]
        list2 = [40, 30, 20, 10]
        col1 = "Дата"
        col2 = "Сотрудник"
        col3 = "Сообщение"
        data = pd.DataFrame({col1: list1, col2: list2})
        data.to_excel(xlName, sheet_name="sheet1", index=False)
        # # Указать writer библиотеки
        # writer = pd.ExcelWriter(xlName, engine='xlsxwriter')

        # # Записать ваш DataFrame в файл     
        # yourData.to_excel(writer, 'Sheet1')

        # # Сохраним результат 
        # writer.save()
        pass
