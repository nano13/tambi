# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem
from QCustomizedWidgets.QInputLine import QInputLine

from interpreter.interpreter import Interpreter
#from interpreter.structs import Result

class QCoreTab(QWidget):
    
    interpreter = Interpreter()
    
    def __init__(self):
        super().__init__()
        
    def tableTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        self.table = QTableWidget()
        
        grid.addWidget(self.table, 0, 0)
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        grid.addWidget(line, 1, 0)
        
        return self
    
    def commandEntered(self, command):
        print("command:", command)
        result = self.interpreter.interpreter(command)
        
        if result.error != None:
            pass
        elif result.category == "table":
            self.resultInTable(result)
        
    def resultInTable(self, result):
        
        self.table.setRowCount(len(result.payload))
        self.table.setColumnCount(len(result.payload[0]))
        
        self.table.setHorizontalHeaderLabels(result.header)
        
        for row, line in enumerate(result.payload):
            for column, item in enumerate(line):
                self.table.setItem(row, column, QTableWidgetItem(str(item)))
                
        self.table.resizeColumnsToContents()