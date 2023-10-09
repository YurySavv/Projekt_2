from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from ten_pt4 import Ui_Dialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(791, 574)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 330, 761, 191))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 181, 281))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 20, 201, 281))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(410, 20, 191, 281))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(614, 20, 161, 281))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Категории"))
        self.pushButton_2.setText(_translate("MainWindow", "Склады"))
        self.pushButton_3.setText(_translate("MainWindow", "Заказы"))
        self.pushButton_4.setText(_translate("MainWindow", "Выбрать операцию"))
        self.pushButton_5.setText(_translate("MainWindow", "Клиенты"))
        self.pushButton.clicked.connect(partial(self.table_dialog, 'Category', "2"))
        self.pushButton_2.clicked.connect(partial(self.table_dialog, 'Warehouses', "2"))
        self.pushButton_3.clicked.connect(partial(self.table_dialog, 'Orders', "3"))
        self.pushButton_4.clicked.connect(partial(self.table_dialog, 'Choose_operation', "4"))
        self.pushButton_5.clicked.connect(partial(self.table_dialog, 'Clients', "5"))

    # функция для передачи данных через кнопку, в данном случае передается название таблицы
    def table_dialog(self, arg1, arg2):
        print(arg1, arg2)
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.table_name = arg1
        ui_table.setupUi(Dialog)


        Dialog.show()
        Dialog.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
