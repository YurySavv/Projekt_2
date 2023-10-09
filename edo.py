import os
from docx import Document
import openpyxl
import json
from datetime import datetime

with open('path.json', 'r', encoding='utf-8') as f:
    text = json.load(f)


def gen_edo(type_oper, bd_index):
    path = text[type_oper]
    wb = openpyxl.Workbook()
    document = Document()
    if os.path.exists(path.split('\\')[0]):
        pass
    else:
        os.mkdir(path.split('\\')[0])
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    now = datetime.now()
    date_creation = str(now)[:10]

    wb.create_sheet(title=f'{type_oper}', index=0)
    wb.remove(wb['Sheet'])
    wb.save(f'{path}\\№_{bd_index}_{date_creation}.xlsx')
    os.startfile(f'{path}\\№_{bd_index}_{date_creation}.xlsx', 'open')
    #  sql запрос на создание записи в бд

    document.save(f'{path}\\№_{bd_index}_{date_creation}.docx')
    os.startfile(f'{path}\\№_{bd_index}_{date_creation}.docx', 'open')
    #  sql запрос на создание записи в бд


# generation_Word('Приемка_товара', 5)
gen_edo('Приемка_товара', 8)
