
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

from QCustomizedWidgets.QFreehandDrawWidget import QFreehandDrawWidget


class QNewDeckWidget(QWidget):
    
    selectLanguage = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def newDeckPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        language_select_button = QPushButton("select language")
        language_select_button.clicked.connect(self.languageSelectButtonClicked)
        
        self.freehandDrawWidget = QFreehandDrawWidget()
        
        grid.addWidget(language_select_button, 0, 0)
        grid.addWidget(self.freehandDrawWidget, 1, 0, 1, 3)
        
        return self
    
    def languageSelectButtonClicked(self):
        self.selectLanguage.emit()
