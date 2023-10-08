import os
from docx import Document
import openpyxl
import json

with open('path.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
    text = json.load(f)

str1 = 'Продажа, Приемка_товара, Перемещение, Списание_товара'


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

    wb.create_sheet(title=f'{type_oper}', index=0)
    wb.remove(wb['Sheet'])
    wb.save(f'{path}\\{bd_index}.xlsx')
    os.startfile(f'{path}\\{bd_index}.xlsx', 'open')

    document.save(f'{path}\\{bd_index}.docx')
    os.startfile(f'{path}\\{bd_index}.docx', 'open')


# generation_Word('Приемка_товара', 5)
gen_edo('Приемка_товара', 8)
