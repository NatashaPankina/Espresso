import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from UI.main import Ui_MainWindow1
from UI.addEditCoffeeForm import Ui_MainWindow2


list1 = ['Светлая', 'Средняя', 'Сильная']
list2 = ['в зернах', 'молотый']


class MyWidget(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn1.clicked.connect(self.run1)
        self.btn2.clicked.connect(self.run2)
        self.initUI()

    def initUI(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM table_coffee""").fetchall()
        self.tw.setRowCount(0)
        for i, row in enumerate(res):
            self.tw.setRowCount(self.tw.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tw.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()

    def run1(self):
        self.add = Add(self)
        self.add.show()       

    def run2(self):
        self.change = Change(self)
        rows = list(set([i.row() for i in self.tw.selectedItems()]))
        if len(rows) == 0:
            self.label1.setText('Для изменения поля его необходимо выбрать')
        elif len(rows) > 1:
            self.label1.setText('Выберите одно поле')
        else:
            self.label1.clear()
            self.change.show()



class Add(QMainWindow, Ui_MainWindow2):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setupUi(self)
        self.btn1.clicked.connect(self.run)
        
    def run(self):
        a = self.line1.text()
        b = self.cb1.currentText()
        c = self.cb2.currentText()
        d = self.line2.text()
        e = self.line3.text()
        f = self.line4.text()
        if len(d) == 0 or len(a) == 0 or len(e) == 0 or not(e.isdigit()) or not(f.isdigit()) or len(f) == 0:
            self.label.setText('Неверно заполнена форма')
        elif int(f) < 0 or int(e) < 0:
            self.label.setText('Неверно заполнена форма')
        else:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            cur.execute("""INSERT INTO table_coffee(sort, roast, grains, taste, price, size) VALUES (?, ?, ?, ?, ?, ?)""", (a, b, c, d, e, f))
            con.commit()
            con.close()
            MyWidget.initUI(self.name)
            self.close()


class Change(QMainWindow, Ui_MainWindow2):
    def __init__(self, name):
        super().__init__()
        self.name = name    
        self.setupUi(self)
        self.btn1.clicked.connect(self.run)
        self.initUI()

    def initUI(self):
        rows = list(set([i.row() for i in self.name.tw.selectedItems()]))
        ids = [self.name.tw.item(i, 0).text() for i in rows]
        if len(rows) != 0:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            res = cur.execute("""SELECT sort, roast, grains, taste, price, size FROM table_coffee WHERE ID = ?""", (ids[0],)).fetchall()
            ind1 = list1.index(res[0][1])
            ind2 = list2.index(res[0][2])
            self.line1.setText(res[0][0])
            self.line2.setText(str(res[0][3]))
            self.cb1.setCurrentIndex(ind1)
            self.cb2.setCurrentIndex(ind2)
            self.line3.setText(str(res[0][4]))
            self.line4.setText(str(res[0][5]))
            con.close()

    def run(self):
        rows = list(set([i.row() for i in self.name.tw.selectedItems()]))
        ids = [self.name.tw.item(i, 0).text() for i in rows]
        a = self.line1.text()
        b = self.cb1.currentText()
        c = self.cb2.currentText()
        d = self.line2.text()
        e = self.line3.text()
        f = self.line4.text()
        if len(d) == 0 or len(a) == 0 or len(e) == 0 or not(e.isdigit()) or not(f.isdigit()) or len(f) == 0:
            self.label.setText('Неверно заполнена форма')
        elif int(f) < 0 or int(e) < 0:
            self.label.setText('Неверно заполнена форма')
        else:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            cur.execute("""UPDATE table_coffee SET sort = ?, roast = ?, grains = ?, taste = ?, price = ?, size = ?
                           WHERE ID = ?""", (a, b, c, d, e, f, ids[0]))
            con.commit()
            con.close()
            MyWidget.initUI(self.name)
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())