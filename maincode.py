import os.path
import sys,os
import sqlite3

from PyQt5.QtWidgets import *

def resources_path(relative_path):
    base_path = getattr(sys, '_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)

from PyQt5.uic import loadUiType

FORM_CLASS,_= loadUiType(resources_path("maindesign.ui"))
x = 0
idx = 3

class Main(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_button()
        self.navigate()
        self.aqua_theme()

    def handle_button(self):
        self.refresh_btn.clicked.connect(self.get_data)
        self.search_btn.clicked.connect(self.search)
        self.check_btn.clicked.connect(self.level)
        self.update_btn.clicked.connect(self.update)
        self.delete_btn.clicked.connect(self.delete)
        self.add_btn.clicked.connect(self.add)
        self.first_btn.clicked.connect(self.first)
        self.last_btn.clicked.connect(self.last)
        self.next_btn.clicked.connect(self.next)
        self.previous_btn.clicked.connect(self.previous)
        self.light.toggled.connect(self.aqua_theme)
        self.dark.toggled.connect(self.dark_blue)

    def get_data(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = '''SELECT * from parts'''

        result = cursor.execute(command)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))

        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_nbr = ''' SELECT COUNT(DISTINCT PartName) from parts '''
        ref_nbr = ''' SELECT COUNT(DISTINCT Reference) from parts '''

        result_ref_nbr = cursor2.execute(ref_nbr)
        result_parts_nbr = cursor3.execute(parts_nbr)

        self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0]))
        self.lbl_parts_nbr.setText(str(result_parts_nbr.fetchone()[0]))

        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_hole = '''SELECT MIN(NumberOfHoles), Reference from parts'''
        max_hole = '''SELECT MAX(NumberOfHoles), Reference from parts'''

        result_min_hole = cursor4.execute(min_hole)
        result_max_hole = cursor5.execute(max_hole)

        r1 = result_min_hole.fetchone()
        r2 = result_max_hole.fetchone()

        self.lbl_min_hole.setText(str(r1[0]))
        self.lbl_max_hole.setText(str(r2[0]))

        self.lbl_min_hole_2.setText(str(r1[1]))
        self.lbl_max_hole_2.setText(str(r2[1]))

    def level(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT Reference, PartName, Count from parts order by Count asc LIMIT 3 '''

        result = cursor.execute(command)

        self.table2.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        nbr = int(self.count_filter_txt.text())

        command = '''SELECT * from parts WHERE COUNT<=?'''

        result = cursor.execute(command, [nbr])

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def navigate(self):
        global idx
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = '''SELECT * from  parts WHERE ID=?'''

        result = cursor.execute(command, [idx])
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.number_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])

    def update(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        id_ = int(self.id.text())
        reference_ = self.reference.text()
        part_name_ = self.part_name.text()
        min_area_ = self.min_area.text()
        max_area_ = self.max_area.text()
        number_of_holes_ = self.number_of_holes.text()
        min_diameter_ = self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())

        row = (reference_, part_name_, min_area_, max_area_, number_of_holes_, min_diameter_, max_diameter_, count_, id_)

        command = ''' UPDATE parts SET Reference=?,PartName=?,MinArea=?,MaxArea=?,NumberOfHoles=?,MinDiameter=?,MaxDiameter=?,Count=? WHERE ID=?'''

        cursor.execute(command, row)

        db.commit()

    def delete(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        d = self.id.text()

        query = '''DELETE FROM parts WHERE ID = ?'''

        cursor.execute(query, [d])

        db.commit()

    def add(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        reference_ = self.reference.text()
        part_name_ = self.part_name.text()
        min_area_ = self.min_area.text()
        max_area_ = self.max_area.text()
        number_of_holes_ = self.number_of_holes.text()
        min_diameter_ = self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())

        row = (reference_, part_name_, min_area_, max_area_, number_of_holes_, min_diameter_, max_diameter_, count_)

        command = ''' INSERT INTO parts (Reference,PartName,MinArea,MaxArea,NumberOfHoles,MinDiameter,MaxDiameter,Count) VALUES (?,?,?,?,?,?,?,?)'''

        cursor.execute(command, row)

        db.commit()

    def first(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT * from  parts  order by ID ASC '''

        result = cursor.execute(command)
        row = result.fetchone()

        self.id.setText(str(row[0]))
        self.reference.setText(str(row[1]))
        self.part_name.setText(str(row[2]))
        self.min_area.setText(str(row[3]))
        self.max_area.setText(str(row[4]))
        self.number_of_holes.setText(str(row[5]))
        self.min_diameter.setText(str(row[6]))
        self.max_diameter.setText(str(row[7]))
        self.count.setValue(row[8])

    def last(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT * from  parts  order by ID DESC '''

        result = cursor.execute(command)
        row = result.fetchone()

        self.id.setText(str(row[0]))
        self.reference.setText(str(row[1]))
        self.part_name.setText(str(row[2]))
        self.min_area.setText(str(row[3]))
        self.max_area.setText(str(row[4]))
        self.number_of_holes.setText(str(row[5]))
        self.min_diameter.setText(str(row[6]))
        self.max_diameter.setText(str(row[7]))
        self.count.setValue(row[8])

    def next(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = '''SELECT ID from parts'''
        result = cursor.execute(command)

        val = result.fetchall()
        total = len(val)
        global x
        global idx
        x += 1
        if x < total:
            idx = val[x][0]
            self.navigate()
        else:
            x = total-1
            print("End of file")

    def previous(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = '''SELECT ID from parts'''
        result = cursor.execute(command)

        val = result.fetchall()
        global x
        global idx
        x = x - 1
        if x > -1:
            idx = val[x][0]
            self.navigate()
        else:
            x = 0
            print("End of file")

    def aqua_theme(self):
        style = open('themes/Aqua.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_blue(self):
        style = open('themes/dark_blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    Window = Main()
    Window.show()
    app.exec_()

if __name__ == '__main__':
    main()