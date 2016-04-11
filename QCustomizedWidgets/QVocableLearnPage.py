# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QPushButton
from PyQt5.Qt import Qt
#import PyQt5.QtGui
from PyQt5.QtGui import QFont

class QVocableLearnPage(QWidget):
    def __init__(self):
        super().__init__()
        
    def vocableLearnPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        self.vocable_list = ["a", "b", "c", "d"]
        self.translation_list = ["1", "2", "3", "4"]
        self.vocable_counter = 0
        
        self.current_vocable = QLabel()
        #self.current_vocable.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.current_vocable.setFont(QFont("Helvetica", 16))
        self.current_vocable.setText(self.vocable_list[self.vocable_counter])
        self.current_vocable.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        self.current_translation = QLabel()
        #self.current_translation.setText(self.translation_list[self.vocable_counter])
        self.current_translation.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        
        self.prev_button = QPushButton("prev")
        self.next_button = QPushButton("next")
        self.show_button = QPushButton("show")
        
        self.prev_button.clicked.connect(self.prevButtonClicked)
        self.next_button.clicked.connect(self.nextButtonClicked)
        self.show_button.clicked.connect(self.showButtonClicked)
        
        grid.addWidget(self.current_vocable, 0, 1)
        grid.addWidget(self.current_translation, 1, 1)
        grid.addWidget(self.show_button, 2, 1)
        grid.addWidget(self.prev_button, 3, 0)
        grid.addWidget(self.next_button, 3, 2)
        
        return self
    
    def showNewVocables(self, vocable_list, translation_list):
        self.vocable_list = vocable_list;
        self.translation_list = translation_list;
        self.vocable_counter = 0
    
    def prevButtonClicked(self, button):
        if self.vocable_counter > 0:
            self.vocable_counter -= 1
            self.current_vocable.setText(self.vocable_list[self.vocable_counter])
            self.current_translation.setText("")
        
    def nextButtonClicked(self, button):
        if self.vocable_counter < len(self.vocable_list)-1:
            self.vocable_counter += 1
            self.current_vocable.setText(self.vocable_list[self.vocable_counter])
            self.current_translation.setText("")
        else:
            pass
        
    def showButtonClicked(self, button):
        self.current_translation.setText(self.translation_list[self.vocable_counter])
