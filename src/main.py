from PyQt5.QtCore import reset
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3 as sql
import sys

# Veritabanı Görüntüleyicisi

class Window(QWidget):
    def __init__(self, title, shape, icon):
        super().__init__()
        self.title = title
        self.x, self.y, self.w, self.h = shape
        self.icon = QIcon(icon)
        self.db = ""
        self.hbox = QHBoxLayout()
        self.initUI()
        self.setLayout(self.hbox)
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setGeometry(self.x, self.y, self.w, self.h)

        self.open_btn = QPushButton(text="Open Database", clicked=self.OpenDatabase)
        self.tables_box = QComboBox()
        self.tables_box.currentIndexChanged.connect(lambda : self.GetDataBase(self.tables_box.currentText()))

        vbox = QVBoxLayout()
        vbox.addWidget(self.open_btn)
        vbox.addWidget(self.tables_box)
        vbox.addStretch()

        self.hbox.addLayout(vbox)
        
        self.table = QTableWidget()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hbox.addWidget(self.table)

    def OpenDatabase(self):
        dlg = QFileDialog()
        
        dlg.exec_()
        self.db = dlg.selectedFiles()[0]
        self.conn = sql.connect(self.db)
        self.cursor = self.conn.cursor()
        
        self.GetTables()

    def GetTables(self):
        sqlquery = "select name from sqlite_master where type = 'table'"
        tables = self.cursor.execute(sqlquery)
        tables = tables.fetchall()
        for table in tables:
            self.tables_box.addItem(table[0])

    def GetDataBase(self, table):
        sqlquery = f"select * from {table}"
        rows = self.cursor.execute(sqlquery).fetchall()

        sqlquery = f"pragma table_info({table});"
        lines = self.cursor.execute(sqlquery).fetchall()

        column_names = []
        for line in lines:
            column_name = line[1]
            column_names.append(column_name)

        self.table.setColumnCount(len(lines))
        self.table.setRowCount(len(rows))

        self.table.setHorizontalHeaderLabels(list(column_names))

        row_state = 0
        col_state = 0
        for row in rows:
            for col in row:
                self.table.setItem(row_state, col_state, QTableWidgetItem(col))
                col_state += 1
            col_state = 0
            row_state += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window("DBrowser", (100, 100, 500, 500), "../img/icon.png")
    app.setStyle("Windows")
    app.exec_()