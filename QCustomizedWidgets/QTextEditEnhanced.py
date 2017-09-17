
from PyQt5.QtWidgets import QTextEdit

class QTextEditEnhanced(QTextEdit):
    
    zoom_counter = 0
    original_size = None
    
    def __init__(self):
        super().__init__()
    
    def zoomIn(self):
        size = self.fontPointSize()
        if not self.original_size:
            self.original_size = size
        
        if size == 0.0:
            self.zoom_counter += 1
            super().zoomIn()
        else:
            cursor = self.textCursor()
            self.selectAll()
            self.setFontPointSize(size +1)
            cursor.clearSelection()
            self.setTextCursor(cursor)
    
    def zoomOut(self):
        size = self.fontPointSize()
        if not self.original_size:
            self.original_size = size
        
        if size == 0.0:
            self.zoom_counter -= 1
            super().zoomOut()
        else:
            cursor = self.textCursor()
            self.selectAll()
            self.setFontPointSize(size -1)
            cursor.clearSelection()
            self.setTextCursor(cursor)
    
    def zoomReset(self):
        size = self.fontPointSize()
        if size == 0.0:
            if self.zoom_counter < 0:
                for i in range(abs(self.zoom_counter)):
                    self.zoomIn()
            
            else:
                for i in range(self.zoom_counter):
                    self.zoomOut()
        
        else:
            cursor = self.textCursor()
            self.selectAll()
            self.setFontPointSize(self.original_size)
            cursor.clearSelection()
            self.setTextCursor(cursor)
    
