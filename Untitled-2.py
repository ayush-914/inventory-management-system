from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtWidgets 
from PyQt5.QtCore import * 
from PyQt5 import QtCore 
from PyQt5.QtWidgets import QMainWindow 
from PyQt5.QtWidgets import QApplication 


import sys, os
from os import path
from PyQt5.uic import loadUiType 
import sqlite3 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

FORM_CLASS, _ = loadUiType(resource_path("main.ui"))


class Main(QMainWindow, FORM_CLASS): 
    def _init_(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.NAVIGATE()
    

    def Handel_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)
        self.check_btn.clicked.connect(self.LEVEL)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)
    

    def GET_DATA(self): 
        db = sqlite3.connect(resource_path("final_parts_table.db"))
        cursor = db.cursor() 

        command = ''' SELECT * from data '''
        result = cursor.execute(command)
        self.table.setRowCount(0) 

        
        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_nbr = ''' SELECT COUNT (DISTINCT PartName) from data '''
        ref_nbr = ''' SELECT COUNT (DISTINCT Reference) from data '''

        result_ref_nbr = cursor2.execute(ref_nbr)
        result_part_nbr = cursor3.execute(parts_nbr)

        self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0]))
        self.lbl_parts_nbr.setText(str(result_part_nbr.fetchone()[0]))

        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_hole = ''' SELECT MIN(NumberOfHoles), Reference from data'''
        max_hole = ''' SELECT MAX(NumberOfHoles), Reference from data'''

        result_min_hole = cursor4.execute(min_hole)
        result_max_hole = cursor5.execute(max_hole)

        r1 = result_min_hole.fetchone()
        r2 = result_max_hole.fetchone()
    
        self.lbl_min_holes.setText(str(r1[0]))
        self.lbl_max_holes.setText(str(r2[0]))

        self.lbl_min_holes_2.setText(str(r1[1]))
        self.lbl_max_holes_2.setText(str(r2[1]))


    def SEARCH(self): 
        db = sqlite3.connect(resource_path("final_parts_table.db"))
        cursor = db.cursor()

        nbr = int(self.count_filter_txt.text())
        command = ''' SELECT * from data WHERE count <= ?'''
        result = cursor.execute(command,[nbr])
        self.table.setRowCount(0) 

        for row_number, row_data in enumerate(result): 
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data): 
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    
    def NAVIGATE(self): 
        db = sqlite3.connect(resource_path("final_parts_table.db"))
        cursor = db.cursor()

        command = ''' SELECT * from data'''
        result = cursor.execute(command)
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
