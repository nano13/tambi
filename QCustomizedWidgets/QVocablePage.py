# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget

class QVocablePage(QWidget):
    def __init__(self):
        super().__init__()
        
    def vocableLearnPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        self.current_vocable = QTableWidget()
        
        #self.current_vocable.setText("bla")
        
        grid.addWidget(self.current_vocable, 0, 1)
        
        return self