import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM table_coffee""").fetchall()
        self.tw.setRowCount(0)
        for i, row in enumerate(res):
            self.tw.setRowCount(self.tw.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tw.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())