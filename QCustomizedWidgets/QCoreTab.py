# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon
from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QItemizedWidget import QItemizedWidget
from QCustomizedWidgets.QVirtualKeyboardWindow import QVirtualKeyboardWindow

from interpreter.interpreter import Interpreter
from interpreter.exceptions import ClearCalled

from misc.unicodeFonts import UnicodeFonts

from functools import partial

from QCustomizedWidgets.QBeamerWindow import QBeamerWindow
from QCustomizedWidgets.QMusicBeamerWidget import QMusicBeamerWidget

class QCoreTab(QWidget):
    
    interpreter = Interpreter()
    beamer = None
    
    def __init__(self):
        super().__init__()
        self.unicode_fonts = UnicodeFonts()
        
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
        
        self.unicode_fonts.applyFontAndSizeToQWidget(data, self.editor)
        
        self.editor.setText(data)
        
        return self
    
    def vocableTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        self.vocable_page = QVocableStackedWidget().vocableWidget()
        grid.addWidget(self.vocable_page, 0, 0)
        
        return self
    
    def musicBeamerTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        music_beamer_widget = QMusicBeamerWidget()
        grid.addWidget(music_beamer_widget, 0, 0)
        
        return self
    
    def amazingGraceTab(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        import os
        base, dirs, files = next(iter(os.walk('./amazing_grace')))
        max_i = 0
        for i, f in enumerate(sorted(files)):
            label = str(f.split('.')[0])
            button = QPushButton(label)
            if i < len(files)/2:
                grid.addWidget(button, i, 0)
            else:
                grid.addWidget(button, i-len(files)/2, 1)
            button.clicked.connect(partial(self.amazingGraceButtonClicked, label))
            max_i += 1
            
        blank = QPushButton('blank')
        grid.addWidget(blank, max_i, 0, 1, 2)
        blank.clicked.connect(self.beamerCanvasBlank)
        return self
    def amazingGraceButtonClicked(self, language):
        if not self.beamer == None:
            self.beamer.destroy()
        
        fobj = open('./amazing_grace/'+str(language)+'.tex', 'r')
        text = ''
        for line in fobj:
            text += line.replace('\\\\', '')
        
        canvas = QBeamerWindow()
        canvas.setText(text)
        canvas.routeToScreen()
        self.beamer = canvas
        canvas.showFullScreen()
    def beamerCanvasBlank(self):
        if not self.beamer == None:
            self.beamer.destroy()
    
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
        try:
            result = self.interpreter.interpreter(command)
        except ClearCalled:
            self.clearDisplayWidget()
        else:
            if hasattr(result, 'error') and result.error:
                self.showErrorMessage(result.error)
            elif result is None:
                self.showErrorMessage('no result found')
            elif hasattr(result, 'category') and result.category == "table":
                try:
                    result.payload[0]
                except IndexError:
                    pass # datastructure does not fit to display type 'table'
                else:
                    self.resultInTable(result)
            elif hasattr(result, 'category') and result.category == "list":
                self.resultInTextEdit(result)
            elif hasattr(result, 'category') and result.category == "text":
                self.resultInTextEdit(result)
            elif hasattr(result, 'category') and result.category == "string":
                self.resultInTextEdit(result)
            elif hasattr(result, 'category') and result.category == "itemized":
                self.resultInItemizedWidget(result)
    
    def clearDisplayWidget(self):
        self.display_widget.deleteLater()
        self.display_widget = QTextEdit()
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
    
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
                table_item = QTableWidgetItem(str(item))
                self.unicode_fonts.applyFontToQWidget(str(item), table_item)
                self.display_widget.setItem(row, column, table_item)
        
        self.display_widget.resizeColumnsToContents()
        self.addDisplayWidget()
    
    def resultInTextEdit(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QTextEdit()
        
        self.unicode_fonts.applyFontAndSizeToQWidget(result.toString(), self.display_widget)
        
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
    
