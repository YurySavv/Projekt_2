import sys
import sqlite3
from PyQt5 import QtWidgets


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()
        return data

    def __del__(self):
        self.conn.close()


class TableDialog(QtWidgets.QDialog):
    def __init__(self, table_name, data):
        super().__init__()
        self.setWindowTitle(table_name)
        self.setMinimumWidth(600)  # Минимальная ширина диалогового окна
        self.setMinimumHeight(400)  # Минимальная высота диалогового окна

        layout = QtWidgets.QVBoxLayout()
        table_widget = QtWidgets.QTableWidget()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        # Установка размеров ячеек таблицы
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        table_widget.verticalHeader().setDefaultSectionSize(50)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))

        layout.addWidget(table_widget)

        # Добавление кнопок "Удалить", "Добавить", "Изменить", "Поиск товара"
        delete_button = QtWidgets.QPushButton('Удалить')
        add_button = QtWidgets.QPushButton('Добавить')
        edit_button = QtWidgets.QPushButton('Изменить')
        search_button = QtWidgets.QPushButton('Поиск товара')

        layout.addWidget(delete_button)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(search_button)

        # Подключение кнопок к функциям
        delete_button.clicked.connect(self.delete_item)
        add_button.clicked.connect(self.add_item)
        edit_button.clicked.connect(self.edit_item)
        search_button.clicked.connect(self.search_item)

        self.setLayout(layout)

    def delete_item(self):
        # Реализация удаления записи из базы данных
        pass

    def add_item(self):
        # Реализация добавления новой записи в базу данных
        pass

    def edit_item(self):
        # Реализация редактирования записи в базе данных
        pass

    def search_item(self):
        # Реализация поиска товара
        pass


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 300)  # Установка размеров окна
        layout = QtWidgets.QVBoxLayout()
        products_button = QtWidgets.QPushButton('Продукты')
        warehouses_button = QtWidgets.QPushButton('Склады')
        clients_button = QtWidgets.QPushButton('Клиенты')
        orders_button = QtWidgets.QPushButton('Заказы')

        # Установка размеров кнопок
        button_width = 200
        button_height = 60
        products_button.setFixedSize(button_width, button_height)
        warehouses_button.setFixedSize(button_width, button_height)
        clients_button.setFixedSize(button_width, button_height)
        orders_button.setFixedSize(button_width, button_height)

        layout.addWidget(products_button)
        layout.addWidget(warehouses_button)
        layout.addWidget(clients_button)
        layout.addWidget(orders_button)

        products_button.clicked.connect(lambda: self.show_table_dialog('Products'))
        warehouses_button.clicked.connect(lambda: self.show_table_dialog('Warehouses'))
        clients_button.clicked.connect(lambda: self.show_table_dialog('Customers'))
        orders_button.clicked.connect(lambda: self.show_table_dialog('Orders'))

        self.setLayout(layout)

    def show_table_dialog(self, table_name):
        data = self.db_manager.get_data(table_name)
        dialog = TableDialog(table_name, data)
        dialog.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.db_manager = DatabaseManager('inventory_management.db')
    main_window.show()
    sys.exit(app.exec_())
