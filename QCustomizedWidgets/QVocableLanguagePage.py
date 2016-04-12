
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from functools import partial
from PyQt5.QtCore import pyqtSignal
from modules.vocable.vocableDbAdapter import VocableDbAdapter

class QVocableLanguagePage(QWidget):
    
    languageSelected = pyqtSignal(str, name='languageSelected')
    
    dbAdapter = VocableDbAdapter()
    
    def __init__(self):
        super().__init__()
        
        
    def vocableLanguagePage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        label_list = self.getLanguages()
        button_list = []
        for i, label in enumerate(label_list):
            button = QPushButton(label, self)
            button_list.append(button)
            
            grid.addWidget(button_list[i], i, 0)
            button_list[i].clicked.connect(partial(self.buttonClicked, label))
        
        return self
    
    def buttonClicked(self, label):
        self.languageSelected.emit(label)
        
    def getLanguages(self):
        languages = self.dbAdapter.getAvailableLanguages()
        
        return languages
