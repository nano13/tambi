# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon
from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QItemizedWidget import QItemizedWidget
from QCustomizedWidgets.QVirtualKeyboardWindow import QVirtualKeyboardWindow

from interpreter.interpreter import Interpreter

from misc.unicodeFonts import UnicodeFonts

from functools import partial

class QCoreTab(QWidget):
    
    interpreter = Interpreter()
    
    def __init__(self):
        super().__init__()
    
    def editorTab(self, filepath):
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grid)
        
        self.editor = QTextEdit()
        grid.addWidget(self.editor, 0, 0)
        
        fobj = open(filepath[0])
        data = ""
        for line in fobj:
            data += line
        
        unicode_fonts = UnicodeFonts()
        unicode_fonts.applyFontSizeToQWidget(data, self.editor)
        
        self.editor.setText(data)
        
        return self
    
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
        
        self.display_widget = QTextEdit()
        self.display_widget.setText("type in the command 'man' for getting started ...")
        self.display_widget.setReadOnly(True)
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
        
        if hasattr(result, 'error') and result.error:
            self.showErrorMessage(result.error)
        elif result is None:
            self.showErrorMessage('no result found')
        elif hasattr(result, 'category') and result.category == "table":
            self.resultInTable(result)
        elif hasattr(result, 'category') and result.category == "list":
            self.resultInTextEdit(result)
        elif hasattr(result, 'category') and result.category == "text":
            self.resultInTextEdit(result)
        elif hasattr(result, 'category') and result.category == "string":
            self.resultInTextEdit(result)
        elif hasattr(result, 'category') and result.category == "itemized":
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
        
        unicode_fonts = UnicodeFonts()
        unicode_fonts.applyFontSizeToQWidget(result.toString(), self.display_widget)
        
        self.display_widget.setAcceptRichText(True)
        
        self.display_widget.setText(result.toString())
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
    
    def resultInItemizedWidget(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QItemizedWidget(result.payload)
        self.addDisplayWidget()
    
    def showErrorMessage(self, message):
        self.display_widget.deleteLater()
        self.display_widget = QTextEdit()
        self.display_widget.setText(message)
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
    
