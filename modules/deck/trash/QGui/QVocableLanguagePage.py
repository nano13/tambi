
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import Qt

from functools import partial
import os
from modules.vocable.vocableDbAdapter import VocableDbAdapter

class QVocableLanguagePage(QWidget):
    
    grid = None
    
    languageSelected = pyqtSignal(str, name='languageSelected')
    deckLearn = pyqtSignal(str, name='deckLearn')
    deckDirtyDozen = pyqtSignal(str, name='deckDirtyDozen')
    deckView = pyqtSignal(str, name='deckSelected')
    createNewDeckSignal = pyqtSignal()
    
    dbAdapter = VocableDbAdapter()
    defaultDeckPath = None
    
    listWidget = None
    tableWidget = None
    
    def __init__(self):
        super().__init__()
        
        self.tableWidget = QTableWidget()
    
    def setDefaultDeckPath(self, deckpath):
        self.defaultDeckPath = deckpath
    
    def deckPage(self):
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        layout = self.setLayout(self.grid)
        
        self.tableWidget = self.createDeckSelectList()
        self.grid.addWidget(self.tableWidget, 0, 0)
        
        new_deck_button = QPushButton("new deck", self)
        self.grid.addWidget(new_deck_button, 1, 0)
        new_deck_button.clicked.connect(self.createNewDeck)
        
        return self
    
    def rescanLanguageList(self):
        print("rescanning")
        self.tableWidget = self.createDeckSelectList()
    
    def createDeckSelectList(self):
        language_list = self.getLanguages()
        
        self.tableWidget.setRowCount(len(language_list))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        
        for i, label in enumerate(language_list):
            item = QTableWidgetItem(label["name"])
            self.tableWidget.setItem(i, 0, item)
            # for read only:
            item.setFlags(Qt.ItemIsEnabled)
            
            if label["type"] == "deck":
                button_learn_deck = QPushButton("learn", self)
                button_dirty_dozen = QPushButton("dirty dozen", self)
                button_view_deck = QPushButton("view deck", self)
                
                self.tableWidget.setCellWidget(i, 1, button_learn_deck)
                self.tableWidget.setCellWidget(i, 2, button_dirty_dozen)
                self.tableWidget.setCellWidget(i, 3, button_view_deck)
                
                button_learn_deck.clicked.connect(partial(self.tableButtonLearnDeckClicked, label["name"]))
                
                button_dirty_dozen.clicked.connect(partial(self.tableButtonDirtyDozenClicked, label["name"]))
                
                button_view_deck.clicked.connect(partial(self.tableButtonViewDeckClicked, label["name"]))
        
        self.tableWidget.resizeColumnsToContents()
        
        return self.tableWidget
    
    def tableButtonLearnDeckClicked(self, deckname):
        self.deckLearn.emit(deckname)
    
    def tableButtonDirtyDozenClicked(self, deckname):
        self.deckDirtyDozen.emit(deckname)
    
    def tableButtonViewDeckClicked(self, deckname):
        self.deckView.emit(deckname)
    
    def itemClicked(self):
        language = self.listWidget.currentItem().text()
        self.languageSelected.emit(language)
    
    def getLanguages(self):
        languages_dict = []
        dirnames = os.listdir(self.defaultDeckPath)
        for deck in sorted(dirnames):
            languages_dict.append({"name": deck, "type": "deck"})
        
        return languages_dict
    
    def createNewDeck(self):
        self.createNewDeckSignal.emit()
