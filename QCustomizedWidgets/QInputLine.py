# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

class QInputLine(QLineEdit):
    
    return_pressed = pyqtSignal(str, name='return_pressed')
    
    def __init__(self):
        super().__init__()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.return_pressed.emit(self.text())
            self.setText("")
            
        elif e.key() == Qt.Key_Enter:
            self.return_pressed.emit(self.text())
            self.setText("")
        
        super().keyPressEvent(e)