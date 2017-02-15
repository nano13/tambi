# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QIcon
from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QVirtualKeyboardWindow import QVirtualKeyboardWindow

from interpreter.interpreter import Interpreter

from functools import partial

class QCoreTab(QWidget):
    
    interpreter = Interpreter()
    
    def __init__(self):
        super().__init__()
    
    def vocableTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        self.vocable_page = QVocableStackedWidget().vocableWidget()
        grid.addWidget(self.vocable_page, 0, 0)
        
        return self
        
    def cliTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        self.table = QTableWidget()
        self.vkbd = None
        
        grid.addWidget(self.table, 0, 0, 1, 0)
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        grid.addWidget(line, 1, 0)
        
        vkbdButton = QPushButton(self)
        vkbdButton.clicked.connect(partial(self.vkbdButtonClicked, line))
        vkbdButton.setIcon(QIcon.fromTheme('input-keyboard'))
        grid.addWidget(vkbdButton, 1, 1)
        
        return self
    
    def vkbdButtonClicked(self, lineEdit):
        self.vkbd = QVirtualKeyboardWindow()
        self.vkbd.setLineEdit(lineEdit)
    
    def commandEntered(self, command):
        print("command:", command)
        result = self.interpreter.interpreter(command)
        
        print(result)
        print(type(result))
        
        error_happened = False
        try:
            result.error
        except AttributeError:
            self.showErrorMessage('result contains error')
            error_happened = True
        
        #try:
            #len(result)
        #except TypeError:
            #self.showErrorMessage('result is empty')
            #error_happened = True
        
        if result is None:
            self.showErrorMessage('no result found')
        #elif result.error != None:
        #   self.showErrorMessage('result contains error')
        #elif len(result) == 0:
        #   self.showErrorMessage('result is empty')
        elif error_happened:
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
        
    def showErrorMessage(self, message):
        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setItem(0, 0, QTableWidgetItem(str(message)))
        self.table.resizeColumnsToContents()
        
