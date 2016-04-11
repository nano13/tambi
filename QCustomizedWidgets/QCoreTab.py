# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem
from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QVocableLearnPage import QVocableLearnPage

from interpreter.interpreter import Interpreter

class QCoreTab(QWidget):
    
    interpreter = Interpreter()
    
    def __init__(self):
        super().__init__()
        
    def vocableLearnTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        self.vocable_page = QVocableLearnPage().vocableLearnPage()
        
        grid.addWidget(self.vocable_page, 0, 0)
        
        return self
        
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
        
        if result is None:
            pass
        elif result.error != None:
            pass
        elif result.category == "table":
            self.resultInTable(result)
        
    def resultInTable(self, result):
        
        self.table.setRowCount(len(result.payload))
        self.table.setColumnCount(len(result.payload[0]))
        
        try:
            self.table.setHorizontalHeaderLabels(result.header)
        except TypeError:
            pass
        
        for row, line in enumerate(result.payload):
            for column, item in enumerate(line):
                self.table.setItem(row, column, QTableWidgetItem(str(item)))
                
        self.table.resizeColumnsToContents()
