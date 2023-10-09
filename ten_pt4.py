import sqlite3 as sl
from functools import partial


con = sl.connect('st10.db')


from PyQt5 import QtCore, QtGui, QtWidgets

d1 = {'Choose_operation': [['QLineEdit', '', '', 'text()'],
                   ['QLineEdit', '', '', 'text()'],
                   ['QDateEdit', '', '', 'text()'],
                   ['QLineEdit', '', '', 'text()'],
                   ['QComboBox', 'name', 'Orders', 'currentText()']],
      'Orders': [['QLineEdit', '', '', 'text()'],
               ['QLineEdit', '', '', 'text()'],
               ['QLineEdit', '', '', 'text()'],
               ['QLineEdit', '', '', 'text()']],
      'Warehouses': [['QLineEdit', '', '', 'text()'],
                   ['QLineEdit', '', '', 'text()'],
                   ['QLineEdit', '', '', 'text()'],
                   ['QTimeEdit', '', '', 'text()'],
                   ['QComboBox', 'name', 'Orders', 'currentText()']],
      'Clients': [['QLineEdit', '', '', 'text()'],
                  ['QLineEdit', '', '', 'text()'],
                  ['QLineEdit', '', '', 'text()'],
                  ['QDateEdit', '', '', 'text()'],
                  ['QLineEdit', '', '', 'text()']],
      'Category': [['QLineEdit', '', '', 'text()'],
                            ['QDateTimeEdit', '', '', 'text()'],
                            ['QComboBox', 'fio', 'Clients', 'currentText()'],
                            ['QComboBox', 'fio', 'Choose_operation', 'currentText()'],
                            ['QComboBox', 'name', 'Warehouses', 'currentText()']],
      }


# словарь координат
dict_coord = {0: [[50, 50, 51, 20], []], 1: [[260, 50, 170, 21], [260, 90, 171, 30]],
              2: [[600, 50, 170, 21], [600, 90, 231, 30]],
              3: [[50, 200, 170, 21], [50, 240, 141, 30]],
              4: [[260, 200, 170, 21], [260, 240, 170, 30]]}

# class Ui_Dialog_2(object):
#     table_name = 'Orders'
#     row = 0


class Ui_Dialog(object):
    table_name = 'Choose_operation'

    # функция которая задает названия колонкам
    def sql_fighter(self, table_name):
        table_name = self.table_name
        param_list = []
        with con:
            cur = con.cursor()
            cur.execute(f'PRAGMA table_info({table_name})')
            data = cur.fetchall()
            for d in data:
                param_list.append(d[1])
        return param_list

    # функция вытягивания данных для записи их в окно в таблицу
    def get_sql(self):
        table_name = self.table_name
        with con:
            data = con.execute(f'SELECT * FROM {table_name}')
            return data.fetchall()

    # функция удаления записей из таблицы
    def sql_del(self):
        table_name = self.table_name
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 0)
        item = int(item.text())
        if row > -1:
            self.tableWidget.removeRow(row)
            self.tableWidget.selectionModel().clearCurrentIndex()
        with con:
            con.execute(f'DELETE FROM {table_name} WHERE id = {item}')

    def go_to_main_menu(self):
        main_menu_dialog = QtWidgets.QDialog()
        main_menu_ui = Ui_Dialog()
        main_menu_ui.setupUi(main_menu_dialog)

        main_menu_dialog.show()
        Dialog.close()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 600)
        self.dialog = Dialog

        self.pushButton_back = QtWidgets.QPushButton(Dialog)
        self.pushButton_back.setGeometry(QtCore.QRect(710, 10, 141, 31))
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_back.setText("Назад")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 50, 550, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(self.sql_fighter(self.table_name)))
        self.tableWidget.setHorizontalHeaderLabels(self.sql_fighter(self.table_name))




        for row in range(len(self.get_sql())):  # генерация таблицы
            self.tableWidget.insertRow(row)
            self.row = row
            for column in range(len(self.get_sql()[row])):
                item = QtWidgets.QTableWidgetItem(str(self.get_sql()[row][column]))
                self.tableWidget.setItem(row, column, item)


        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(710, 60, 141, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(710, 110, 141, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", f'{self.table_name}'))
        self.pushButton_2.setText(_translate("Dialog", "Добавить новую запись"))
        self.pushButton_3.setText(_translate("Dialog", "Удалить"))
        self.pushButton_3.clicked.connect(self.sql_del)
        self.pushButton_2.clicked.connect(Dialog.close)
        self.pushButton_2.clicked.connect(partial(self.add_sql, f'{self.table_name}', "2"))
        self.pushButton_back.clicked.connect(self.go_to_main_menu)
        # self.pushButton.clicked.connect(self.restart)




    # функция для передачи данных через кнопку, в данном случае передается название таблицы
    def add_sql(self, arg1, arg2):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog_1()
        ui_table.table_name = arg1
        ui_table.setupUi(Dialog)

        Dialog.show()
        Dialog.exec_()

class Ui_Dialog_1(object):
    table_name = 'Category'
    row = 0


    def sql_fighter(self):
        table_name = self.table_name
        param_list = []
        with con:
            cur = con.cursor()
            cur.execute(f'PRAGMA table_info({table_name})')
            data = cur.fetchall()
            for d in data:
                param_list.append(d[1])
        return param_list

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 500)
        font = QtGui.QFont()
        font.setPointSize(15)
        Dialog.setFont(font)
        self.sql_fighter()

        for x1 in dict_coord.keys():
            a = f"""
self.QLabel_{x1} = QtWidgets.QLabel(Dialog)
self.QLabel_{x1}.setGeometry(QtCore.QRect({dict_coord[x1][0][0]},{dict_coord[x1][0][1]},{dict_coord[x1][0][2]},{dict_coord[x1][0][3]}))
self.QLabel_{x1}.setFont(font)
self.QLabel_{x1}.setObjectName("label_{x1}")
"""
            exec(a)

        self.pushButton_search = QtWidgets.QPushButton(Dialog)
        self.pushButton_search.setGeometry(QtCore.QRect(710, 160, 141, 31))
        self.pushButton_search.setObjectName("pushButton_search")
        self.pushButton_search.setText("Поиск товаров")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(600, 350, 181, 51))
        self.pushButton.setObjectName("pushButton")

        a = d1[self.table_name]
        for x in range(1, len(a)):
            widg5 = f"""
self.{d1[self.table_name][x][0]}_{x} = QtWidgets.{d1[self.table_name][x][0]}(Dialog)
self.{d1[self.table_name][x][0]}_{x} .setGeometry(QtCore.QRect({dict_coord[x][1][0]},{dict_coord[x][1][1]},{dict_coord[x][1][2]},{dict_coord[x][1][3]}))
self.{d1[self.table_name][x][0]}_{x} .setObjectName("{d1[self.table_name][x][0]}_{x} ")
with con:
    try:        
        data = con.execute(f'SELECT {d1[self.table_name][x][1]} FROM {d1[self.table_name][x][2]}')
        for y in data.fetchall():
            self.{d1[self.table_name][x][0]}_{x}.addItem(str(y[0]))
    except:
        pass

        """
            exec(widg5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def search_products_by_category(self):
        self.pushButton_search.clicked.connect(self.search_products_by_category)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", f"{self.table_name}"))

        self.pushButton.setText(_translate("Dialog", "Добавить"))
        for x2 in range(len(self.sql_fighter())):
            a1 = f""" 
self.QLabel_{x2}.setText(_translate("Dialog", self.sql_fighter()[{x2}]))"""
            exec(a1)

        self.pushButton_search.clicked.connect(self.search_products_by_category)
        # self.pushButton_back.clicked.connect(self.go_to_main_menu)
        self.pushButton.clicked.connect(self.get_data)
        self.pushButton.clicked.connect(Dialog.close)
        self.pushButton.clicked.connect(partial(self.table_dialog, self.table_name, "2"))


    def table_dialog(self, arg1, arg2):
        print(arg1, arg2)
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.table_name = arg1
        ui_table.setupUi(Dialog)

        Dialog.show()
        Dialog.exec_()

    ### функция вытаскивает данные с виджетов и записывает в БД
    def get_data(self):
        global c1
        list_data = []

        for ik in range(1, len(d1[self.table_name])):
            a1 = f"""
self.{d1[self.table_name][ik][0]}_{ik}.{d1[self.table_name][ik][3]}
"""
            c1 = eval(a1)
            try:
                with con:
                    c1 = con.execute(
                        f"SELECT id FROM {d1[self.table_name][ik][2]} WHERE {d1[self.table_name][ik][1]} ='{c1}'").fetchone()[
                        0]
            except:
                pass

            list_data.append(c1)
        print(list_data)

        try:
            with con:
                con.execute(
                    f'INSERT INTO {self.table_name} SELECT COUNT(*)+1, "{list_data[0]}", "{list_data[1]}","{list_data[2]}", "{list_data[3]}" FROM {self.table_name}')
        except:
            with con:
                con.execute(
                    f'INSERT INTO {self.table_name} SELECT COUNT(*)+1, "{list_data[0]}", "{list_data[1]}","{list_data[2]}" FROM {self.table_name}')

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())