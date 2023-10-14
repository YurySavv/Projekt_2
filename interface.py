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

    def delete_data(self, table_name, item_id):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (item_id,))
        self.conn.commit()

    def insert_data(self, table_name, values, column_name):
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO {table_name} {tuple(column_name)} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def update_data(self, table_name, values, item_id):
        set_values = ', '.join([f"{key} = ?" for key in values.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE id = ?"
        self.cursor.execute(query, list(values.values()) + [item_id])
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 300)
        layout = QtWidgets.QVBoxLayout()
        products_button = QtWidgets.QPushButton('Продукты')
        warehouses_button = QtWidgets.QPushButton('Склады')
        clients_button = QtWidgets.QPushButton('Клиенты')
        orders_button = QtWidgets.QPushButton('Заказы')

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
        data_description = self.get_data_description(table_name)
        data = self.db_manager.get_data(table_name)
        dialog = TableDialog(table_name, data, data_description)
        dialog.db_manager = self.db_manager
        dialog.exec_()

    def get_data_description(self, table_name):
        cursor = self.db_manager.cursor
        cursor.execute(f"PRAGMA table_info({table_name})")
        data_description = cursor.fetchall()
        return data_description

class TableDialog(QtWidgets.QDialog):
    def __init__(self, table_name, data, data_description):
        super().__init__()
        self.setWindowTitle(table_name)
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        self.table_name = table_name
        self.data = data
        self.data_description = data_description

        layout = QtWidgets.QVBoxLayout()

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0]))

        header_labels = [desc[1] for desc in data_description]
        self.table_widget.setHorizontalHeaderLabels(header_labels)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))

        layout.addWidget(self.table_widget)

        delete_button = QtWidgets.QPushButton('Удалить')
        add_button = QtWidgets.QPushButton('Добавить')
        edit_button = QtWidgets.QPushButton('Изменить')

        layout.addWidget(delete_button)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)

        delete_button.clicked.connect(self.delete_item)
        add_button.clicked.connect(self.add_item)
        edit_button.clicked.connect(self.edit_item)

        self.setLayout(layout)

    def delete_item(self):
        selected_item = self.table_widget.currentItem()
        if selected_item is not None:
            row = selected_item.row()
            item_id = self.data[row][0]  # Assuming the first column is the ID
            confirm_dialog = QtWidgets.QMessageBox.question(self, 'Подтверждение удаления',
                                                            f'Вы уверены, что хотите удалить запись с ID {item_id}?',
                                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                            QtWidgets.QMessageBox.No)

            if confirm_dialog == QtWidgets.QMessageBox.Yes:
                self.db_manager.delete_data(self.table_name, item_id)
                self.refresh_data()

    def add_item(self):
        column_names = [desc[1] for desc in self.data_description if desc[1] != 'id']
        dialog = AddItemDialog(column_names)
        if dialog.exec_():
            values = dialog.get_values()
            if all(values):
                self.db_manager.insert_data(self.table_name, values, column_names)
                self.refresh_data()

    def edit_item(self):
        selected_item = self.table_widget.currentItem()
        if selected_item is not None:
            row = selected_item.row()
            item_id = self.data[row][0]  # Assuming the first column is the ID
            column_names = [desc[1] for desc in self.data_description if desc[1] != 'id']
            values = self.data[row][1:]  # Exclude the ID column value
            dialog = EditItemDialog(column_names, values)
            if dialog.exec_():
                updated_values = dialog.get_values()
                self.db_manager.update_data(self.table_name, dict(zip(column_names, updated_values)), item_id)
                self.refresh_data()

    def refresh_data(self):
        self.data = self.db_manager.get_data(self.table_name)
        self.load_data()

    def load_data(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(len(self.data))
        self.table_widget.setColumnCount(len(self.data[0]))

        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                self.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))

class AddItemDialog(QtWidgets.QDialog):
    def __init__(self, column_names):
        super().__init__()
        self.setWindowTitle('Добавить запись')
        self.column_names = column_names

        layout = QtWidgets.QVBoxLayout()

        self.line_edits = []
        for column in column_names:
            label = QtWidgets.QLabel(column)
            line_edit = QtWidgets.QLineEdit()
            layout.addWidget(label)
            layout.addWidget(line_edit)
            self.line_edits.append(line_edit)

        add_button = QtWidgets.QPushButton('Добавить')
        layout.addWidget(add_button)
        add_button.clicked.connect(self.accept)

        cancel_button = QtWidgets.QPushButton('Отмена')
        layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def get_values(self):
        return [line_edit.text() for line_edit in self.line_edits]

class EditItemDialog(QtWidgets.QDialog):
    def __init__(self, column_names, current_values):
        super().__init__()
        self.setWindowTitle('Изменить запись')
        self.column_names = column_names

        layout = QtWidgets.QVBoxLayout()

        self.line_edits = []
        for column, current_value in zip(column_names, current_values):
            label = QtWidgets.QLabel(column)
            line_edit = QtWidgets.QLineEdit(str(current_value))
            layout.addWidget(label)
            layout.addWidget(line_edit)
            self.line_edits.append(line_edit)

        add_button = QtWidgets.QPushButton('Сохранить')
        layout.addWidget(add_button)
        add_button.clicked.connect(self.accept)

        cancel_button = QtWidgets.QPushButton('Отмена')
        layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def get_values(self):
        return [line_edit.text() for line_edit in self.line_edits]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.db_manager = DatabaseManager('inventory_management.db')
    main_window.show()
    sys.exit(app.exec_())
