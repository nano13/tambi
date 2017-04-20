
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore

class QClickLabel(QLabel):
    
    clicked = QtCore.pyqtSignal(int)
    right_clicked = QtCore.pyqtSignal()
    
    pixmap_large = None
    name_id = -1
    
    def __init__(self):
        super().__init__()
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(self.name_id)
            
        if event.button() == QtCore.Qt.RightButton:
            self.right_clicked.emit()
    
