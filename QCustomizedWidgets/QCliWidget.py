
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit, QGraphicsScene
from PyQt5.QtGui import QIcon, QTextFormat

from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QItemizedWidget import QItemizedWidget
from QCustomizedWidgets.QVirtualKeyboardWindow import QVirtualKeyboardWindow

from interpreter.interpreter import Interpreter
from interpreter.exceptions import ClearCalled

from misc.unicodeFonts import UnicodeFonts

from functools import partial

class QCliWidget(QWidget):
    
    interpreter = Interpreter()
    display_widget = None
    vkbd = None
    
    def __init__(self):
        super().__init__()
        
        self.unicode_fonts = UnicodeFonts()
        
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        
        self.display_widget = QTextEdit()
        self.display_widget.setText("type in the command 'man' for getting started ...")
        self.display_widget.setReadOnly(True)
        
        self.addDisplayWidget()
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        self.grid.addWidget(line, 1, 0)
        
        vkbdButton = QPushButton(self)
        vkbdButton.clicked.connect(partial(self.vkbdButtonClicked, line))
        vkbdButton.setIcon(QIcon.fromTheme('input-keyboard'))
        self.grid.addWidget(vkbdButton, 1, 1)
        
        zoomInButton = QPushButton(self)
        zoomInButton.setIcon(QIcon.fromTheme('zoom-in'))
        zoomInButton.clicked.connect(self.onZoomInClicked)
        self.grid.addWidget(zoomInButton, 1, 2)
        
        zoomOutButton = QPushButton(self)
        zoomOutButton.setIcon(QIcon.fromTheme('zoom-out'))
        zoomOutButton.clicked.connect(self.onZoomOutClicked)
        self.grid.addWidget(zoomOutButton, 1, 3)
        
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
        
    def onZoomInClicked(self):
        if type(self.display_widget) == QTextEdit:
            size = self.display_widget.fontPointSize()
            
            if size == 0.0:
                self.display_widget.zoomIn()
            else:
                cursor = self.display_widget.textCursor()
                self.display_widget.selectAll()
                self.display_widget.setFontPointSize(size +1)
                cursor.clearSelection()
                self.display_widget.setTextCursor(cursor)
                
        elif type(self.display_widget) == QTableWidget:
            pass
            #scene = QGraphicsScene()
            #scene.addWidget(self.display_widget)
    
    def onZoomOutClicked(self):
        if type(self.display_widget) == QTextEdit:
            size = self.display_widget.fontPointSize()
            
            if size == 0.0:
                self.display_widget.zoomOut()
            else:
                cursor = self.display_widget.textCursor()
                self.display_widget.selectAll()
                self.display_widget.setFontPointSize(size -1)
                cursor.clearSelection()
                self.display_widget.setTextCursor(cursor)
                
        elif type(self.display_widget) == QTableWidget:
            pass
    
