import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView

DB_NAME = "coffee.db"


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect(DB_NAME)
        self.pushButton.clicked.connect(self.add_elem)
        self.__is_adding_successful = False

    def add_elem(self):
        cur = self.con.cursor()
        try:
            id = cur.execute("SELECT max(id) FROM coffee").fetchone()[0] + 1
            name = self.Name.toPlainText()
            taste = self.Taste.toPlainText()
            price = self.Price.toPlainText()

            if len(name) * len(taste) * len(price) == 0:
                raise ValueError('some lenght == 0')

            new_data = (id, name, taste, price)
            cur.execute("INSERT INTO coffee VALUES (?,?,?,?)", new_data)
            self.__is_adding_successful = True
        except ValueError as ve:
            self.__is_adding_successful = False
            self.errors.setText("Неверно заполнена форма")
        else:
            self.con.commit()
            self.parent().update_result()
            self.close()

    def get_adding_verdict(self):
        return self.__is_adding_successful


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)
        self.con = sqlite3.connect(DB_NAME)
        self.update_result()
        self.pushButton.clicked.connect(self.adding)
        self.add_form = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        que = "SELECT f.id, f.name, f.taste, f.price FROM coffee as f"
        result = cur.execute(que).fetchall()

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['№', 'Название', 'Как на вкус', 'цена'])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
