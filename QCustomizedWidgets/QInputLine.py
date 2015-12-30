# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

from configs.history import History

class QInputLine(QLineEdit):
    
    return_pressed = pyqtSignal(str, name='return_pressed')
    
    history = History()
    history_counter = 0
    
    def __init__(self):
        super().__init__()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.history.historyWrite(self.text())
            self.return_pressed.emit(self.text())
            self.setText("")
            self.history_counter = 0
            
        elif e.key() == Qt.Key_Enter:
            self.history.historyWrite(self.text())
            self.return_pressed.emit(self.text())
            self.setText("")
            self.history_counter = 0
            
        elif e.key() == Qt.Key_Up:
            history_size = self.history.getHistorySize()
            if self.history_counter < history_size:
                self.history_counter += 1
            entry = self.history.historyReadAtIndex(self.history_counter)
            self.setText(entry)
        
        elif e.key() == Qt.Key_Down:
            self.history_counter -= 1
            if self.history_counter < 0:
                self.history_counter = 0
            entry = self.history.historyReadAtIndex(self.history_counter)
            self.setText(entry)
            
        super().keyPressEvent(e)