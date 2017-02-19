# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from modules.vocable.vocableDbAdapter import VocableDbAdapter

class QVocableLearnPage(QWidget):
    
    selectLanguage = pyqtSignal()
    
    dbAdapter = VocableDbAdapter()
    
    current_language = ""
    number_of_vocables = 10
    
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
        self.current_vocable.setFont(QFont("Helvetica", 20))
        self.current_vocable.setText(self.vocable_list[self.vocable_counter])
        self.current_vocable.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        self.current_translation = QLabel()
        #self.current_translation.setText(self.translation_list[self.vocable_counter])
        self.current_translation.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        self.word_counter = QLabel()
        self.word_counter.setText(str(self.vocable_counter+1) + "/" + str(self.number_of_vocables))
        self.word_counter.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        self.language_select_button = QPushButton("select language")
        self.not_want_learn_button = QPushButton("not want to learn")
        self.prev_button = QPushButton("prev")
        self.next_button = QPushButton("next")
        self.show_button = QPushButton("show translation")
        self.known_button = QPushButton("known")
        self.notknown_button = QPushButton("not known")
        self.newset_button = QPushButton("new set")
        
        self.language_select_button.clicked.connect(self.languageSelectButtonClicked)
        self.not_want_learn_button.clicked.connect(self.notWantToLearnClicked)
        self.prev_button.clicked.connect(self.prevButtonClicked)
        self.next_button.clicked.connect(self.nextButtonClicked)
        self.show_button.clicked.connect(self.showButtonClicked)
        self.known_button.clicked.connect(self.knownButtonClicked)
        self.notknown_button.clicked.connect(self.notknownButtonClicked)
        self.newset_button.clicked.connect(self.newsetButtonClicked)
        
        grid.addWidget(self.language_select_button, 0, 0)
        grid.addWidget(self.not_want_learn_button, 0, 1)
        grid.addWidget(self.word_counter, 0, 2)
        #grid.addWidget(self.current_vocable, 1, 1)
        grid.addWidget(self.current_vocable, 1, 0, 1, 3)
        #grid.addWidget(self.current_translation, 2, 1)
        grid.addWidget(self.current_translation, 2, 0, 1, 3)
        grid.addWidget(self.show_button, 3, 1)
        grid.addWidget(self.prev_button, 3, 0)
        grid.addWidget(self.next_button, 4, 0)
        grid.addWidget(self.known_button, 3, 2)
        grid.addWidget(self.notknown_button, 4, 2)
        grid.addWidget(self.newset_button, 4, 1)
        
        return self
    
    def languageSelectButtonClicked(self):
        self.selectLanguage.emit()
        
    def notWantToLearnClicked(self):
        self.dbAdapter.markVocableAsNotToLearn(self.current_language, self.current_vocable.text())
        
    
    def showNewVocables(self, vocable_list, translation_list):
        self.vocable_list = vocable_list;
        self.translation_list = translation_list;
        self.vocable_counter = 0
    
    def prevButtonClicked(self, button):
        if self.vocable_counter > 0:
            self.vocable_counter -= 1
        else:
            self.vocable_counter = len(self.vocable_list)-1
            
        self.current_vocable.setText(self.vocable_list[self.vocable_counter])
        self.current_translation.setText("")
        self.word_counter.setText(str(self.vocable_counter+1) + "/" + str(self.number_of_vocables))
        
    def nextButtonClicked(self, button):
        if self.vocable_counter < len(self.vocable_list)-1:
            self.vocable_counter += 1
        else:
            self.vocable_counter = 0
            
        self.current_vocable.setText(self.vocable_list[self.vocable_counter])
        self.current_translation.setText("")
        self.word_counter.setText(str(self.vocable_counter+1) + "/" + str(self.number_of_vocables))
        
    def showButtonClicked(self, button):
        self.current_translation.setText(self.translation_list[self.vocable_counter])
        
    def knownButtonClicked(self, button):
        self.dbAdapter.updateKnown(self.current_language, self.current_vocable.text(), 1)
        self.dbAdapter.updateLastLearnedDate(self.current_language, self.current_vocable.text())
        self.nextButtonClicked(button)
        
    def notknownButtonClicked(self, button):
        self.dbAdapter.updateKnown(self.current_language, self.current_vocable.text(), -1)
        self.dbAdapter.updateLastLearnedDate(self.current_language, self.current_vocable.text())
        self.nextButtonClicked(button)
        
    def newsetButtonClicked(self, button):
        self.getVocableList(self.current_language)
        self.vocable_counter = 0
        self.word_counter.setText(str(self.vocable_counter+1) + "/" + str(self.number_of_vocables))
        
    def getVocableList(self, language):
        self.current_language = language
        
        self.vocable_counter = 0
        self.vocable_list = []
        self.translation_list = []
        
        #self.vocable_list, self.translation_list = self.dbAdapter.getRandomVocableList(language, 10)
        self.vocable_list, self.translation_list = self.dbAdapter.getIntelligentVocableList(language, 10)
        
        self.current_vocable.setText(self.vocable_list[0])
        self.current_translation.setText("")
