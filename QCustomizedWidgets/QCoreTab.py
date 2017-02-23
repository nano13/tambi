# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon
from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QItemizedWidget import QItemizedWidget
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
        self.grid = QGridLayout()
        #self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        
        self.display_widget = QTableWidget()
        self.vkbd = None
        
        #self.grid.addWidget(self.display_widget, 0, 0, 1, 0)
        self.addDisplayWidget()
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        self.grid.addWidget(line, 1, 0)
        
        vkbdButton = QPushButton(self)
        vkbdButton.clicked.connect(partial(self.vkbdButtonClicked, line))
        vkbdButton.setIcon(QIcon.fromTheme('input-keyboard'))
        self.grid.addWidget(vkbdButton, 1, 1)
        
        return self
    
    def addDisplayWidget(self):
        self.grid.addWidget(self.display_widget, 0, 0, 1, 0)
    
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
        elif result.category == "list":
            self.resultInTextEdit(result)
        elif result.category == "text":
            self.resultInTextEdit(result)
        elif result.category == "itemized":
            self.resultInItemizedWidget(result)
    
    def resultInTable(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QTableWidget()
        self.display_widget.setRowCount(len(result.payload))
        self.display_widget.setColumnCount(len(result.payload[0]))
        
        try:
            self.display_widget.setHorizontalHeaderLabels(result.header)
        except TypeError:
            pass
        
        for row, line in enumerate(result.payload):
            for column, item in enumerate(line):
                self.display_widget.setItem(row, column, QTableWidgetItem(str(item)))
        
        self.display_widget.resizeColumnsToContents()
        self.addDisplayWidget()
    
    def resultInTextEdit(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QTextEdit()
        self.display_widget.setText(result.toString())
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
    
    def resultInItemizedWidget(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QItemizedWidget(result.payload)
        self.addDisplayWidget()
    
    def showErrorMessage(self, message):
        self.display_widget.setRowCount(1)
        self.display_widget.setColumnCount(1)
        self.display_widget.setItem(0, 0, QTableWidgetItem(str(message)))
        self.display_widget.resizeColumnsToContents()
    
