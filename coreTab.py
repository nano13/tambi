# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QLineEdit

class CoreTab(QWidget):
    def __init__(self):
        super().__init__()
        
    def tableTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        table = QTableWidget()
        
        table.setRowCount(100)
        table.setColumnCount(500)
        
        grid.addWidget(table, 0, 0)
        
        line = QLineEdit()
        grid.addWidget(line, 1, 0)
        
        return self