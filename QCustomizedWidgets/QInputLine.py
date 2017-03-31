# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

from configs.history import History

class QInputLine(QLineEdit):
    
    return_pressed = pyqtSignal(str, name='return_pressed')
    
    history = History()
    history_counter = 0
    search_pattern_prefix = ''
    
    def __init__(self):
        super().__init__()
        
    def appendText(self, text):
        prev_text = self.text()
        prev_text += text
        self.setText(prev_text)
        
    def keyPressEvent(self, e):
        #if (e.modifiers() & Qt.NoModifier):
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
            
            if self.history_counter == 1:
                self.search_pattern_prefix = self.text()
                
            if self.text():
                entry = self.history.historyReadWithIndexAndPrefix(self.history_counter, self.search_pattern_prefix)
                if entry == '':
                    self.search_pattern_prefix = ''
                    self.history_counter = 0
            else:
                entry = self.history.historyReadAtIndex(self.history_counter)
            
            self.setText(entry)
        
        elif e.key() == Qt.Key_Down:
            self.history_counter -= 1
            if self.history_counter < 0:
                self.history_counter = 0
            
            if self.search_pattern_prefix:
                entry = self.history.historyReadWithIndexAndPrefix(self.history_counter, self.search_pattern_prefix)
            else:
                entry = self.history.historyReadAtIndex(self.history_counter)
            self.setText(entry)
        else:
            self.history_counter = 0
        
        if (e.modifiers() & Qt.ControlModifier):
            if e.key() == Qt.Key_C:
                self.history_counter = 0
                self.setText("")
        
        super().keyPressEvent(e)
