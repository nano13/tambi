# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget
from QCustomizedWidgets.QInputLine import QInputLine

from interpreter.interpreter import Interpreter

class CoreTab(QWidget):
    
    interpreter = Interpreter()
    
    def __init__(self):
        super().__init__()
        
    def tableTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        table = QTableWidget()
        
        table.setRowCount(100)
        table.setColumnCount(500)
        
        grid.addWidget(table, 0, 0)
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        grid.addWidget(line, 1, 0)
        
        return self
    
    def commandEntered(self, command):
        print("command:", command)
        self.interpreter.interprete(command)