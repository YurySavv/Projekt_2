import sys
from PyQt5 import QtWidgets
import sqlite3

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

class EmployeeSelectionDialog(QtWidgets.QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle('Выберите сотрудника')
        self.setMinimumWidth(400)

        layout = QtWidgets.QVBoxLayout()

        self.employee_combo = QtWidgets.QComboBox()
        employees = self.db_manager.get_data("Employees")
        self.employee_combo.addItems([f"{employee[0]}: {employee[1]}" for employee in employees])

        layout.addWidget(self.employee_combo)

        select_button = QtWidgets.QPushButton('Выбрать')
        layout.addWidget(select_button)
        select_button.clicked.connect(self.select_employee)

        self.setLayout(layout)

    def select_employee(self):
        selected_employee = self.employee_combo.currentText()
        employee_id = int(selected_employee.split(':')[0])
        self.accept(employee_id)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.employee_id = None
        self.db_manager = DatabaseManager('inventory_management.db')
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 300)
        layout = QtWidgets.QVBoxLayout()
        login_button = QtWidgets.QPushButton('Выбрать сотрудника')
        login_button.clicked.connect(self.show_employee_selection)
        layout.addWidget(login_button)
        self.setLayout(layout)

    def show_employee_selection(self):
        employee_selection_dialog = EmployeeSelectionDialog(self.db_manager)
        if employee_selection_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.employee_id = employee_selection_dialog.result()
            self.show_main_menu()

    def show_main_menu(self):
        # Показать основное меню приложения и передать self.employee_id в окна, где это необходимо
        pass  # Реализовать логику отображения основного меню

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
