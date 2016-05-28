
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon

from QCustomizedWidgets.QVirtualKeyboard import QVirtualKeyboard

class QVkbdLineEdit(QWidget):
    def __init__(self):
        super().__init__()
        
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        
        self.lineEdit = QLineEdit(self)
        self.vkbdButton = QPushButton(self)
        self.vkbdButton.clicked.connect(self.vkbdButtonClicked)
        self.vkbdButton.setIcon(QIcon.fromTheme('input-keyboard'))
        
        self.kbd = None
        
        #self.vkbdButton.setFixedSize(30, 30)
        
        grid.addWidget(self.lineEdit, 0, 0)
        grid.addWidget(self.vkbdButton, 0, 1)
        
        self.setLayout(grid)
        
    def setText(self, text):
        self.lineEdit.setText(text)
        
    def appendText(self, text):
        prev_text = self.lineEdit.text()
        "backspace:"
        if text == "\u232b":
            self.lineEdit.setText(prev_text[:-1])
        else:
            prev_text += text
            self.lineEdit.setText(prev_text)
        
    def text(self):
        return self.lineEdit.text()
    
    def vkbdButtonClicked(self):
        self.kbd = QVirtualKeyboard()
        self.kbd.setLineEdit(self)
