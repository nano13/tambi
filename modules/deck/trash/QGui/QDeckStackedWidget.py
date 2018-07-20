
from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

from modules.deck.QGui.QVocableLanguagePage import QVocableLanguagePage
from modules.deck.QGui.QDeckOverviewWidget import QDeckOverviewWidget
from modules.deck.QGui.QDeckItemWidget import QDeckItemWidget
from modules.deck.QGui.QDeckLearnWidget import QDeckLearnWidget
from modules.deck.QGui.QDeckDirtyDozenWidget import QDeckDirtyDozenWidget

from configs.configFiles import ConfigFile

import os

SELECT_DECK_INDEX = 0
DECK_OVERVIEW_INDEX = 1
NEW_DECK_INDEX = 2
DECK_LEARN_INDEX = 3
DECK_DIRTY_DOZEN_INDEX = 4

class QDeckStackedWidget(QWidget):
    
    set_tab_text = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        config = ConfigFile(None, None)
        self.defaultDeckPath = config.readPath("vocable", "deckpath")
        
        while not os.path.exists(self.defaultDeckPath):
            title = "default path for decks needed"
            text = "use " + self.defaultDeckPath + " as path for saving decks?"
            reply = QMessageBox.question(self, title, text, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                os.makedirs(self.defaultDeckPath)
            else:
                folder_path = QFileDialog.getExistingDirectory(self, "Please select Folder for Decks", self.defaultDeckPath)
                
                if folder_path:
                    if not folder_path == self.defaultDeckPath:
                        config.write("vocable", "deckpath", folder_path)
                        self.defaultDeckPath = folder_path
    
    def deckWidget(self):
        self.stack_language_select = QVocableLanguagePage()
        self.stack_language_select.setDefaultDeckPath(self.defaultDeckPath)
        self.stack_language_select.deckPage()
        self.stack_language_select.deckLearn.connect(self.deckLearn)
        self.stack_language_select.deckDirtyDozen.connect(self.deckDirtyDozen)
        self.stack_language_select.deckView.connect(self.deckView)
        self.stack_language_select.createNewDeckSignal.connect(self.createNewDeck)
        
        self.stack_dirty_dozen = QDeckDirtyDozenWidget()
        self.stack_dirty_dozen.selectDeck.connect(self.selectDeck)
        
        self.stack_deck_overview = QDeckOverviewWidget()
        self.stack_deck_overview.selectDeck.connect(self.selectDeck)
        self.stack_deck_overview.createNewItem.connect(self.createNewDeckItem)
        self.stack_deck_overview.editDeckItem.connect(self.editDeckItem)
        
        self.stack_new_deck = QDeckItemWidget()
        self.stack_new_deck.newDeckPage()
        self.stack_new_deck.selectItem.connect(self.deckSelect)
        
        self.stack_deck_learn = QDeckLearnWidget()
        #self.stack_deck_learn.initialize()
        self.stack_deck_learn.selectDeck.connect(self.selectDeck)
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack_language_select)
        self.Stack.addWidget(self.stack_deck_overview)
        self.Stack.addWidget(self.stack_new_deck)
        self.Stack.addWidget(self.stack_deck_learn)
        self.Stack.addWidget(self.stack_dirty_dozen)
        
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        layout = self.setLayout(grid)
        
        grid.addWidget(self.Stack)
        
        return self
    
    def displayWidget(self, i):
        self.Stack.setCurrentIndex(SELECT_DECK_INDEX)
        
        self.set_tab_text.emit("INDEX")
    
    def deckSelect(self, deckname):
        self.stack_deck_overview.initWithDbData()
        self.Stack.setCurrentIndex(DECK_OVERVIEW_INDEX)
        
        self.set_tab_text.emit("view: " + deckname)
    
    def deckDirtyDozen(self, deck):
        self.stack_dirty_dozen.clear()
        
        deckpath = os.path.join(self.defaultDeckPath, deck)
        self.stack_dirty_dozen.initialize(deckpath)
        
        self.Stack.setCurrentIndex(DECK_DIRTY_DOZEN_INDEX)
        
        self.set_tab_text.emit("dd: " + deck)
    
    def deckLearn(self, deck):
        self.stack_deck_learn.clear()
        
        deckpath = os.path.join(self.defaultDeckPath, deck)
        self.stack_deck_learn.initialize(deckpath)
        
        self.Stack.setCurrentIndex(DECK_LEARN_INDEX)
        
        self.set_tab_text.emit("learn: " + deck)
    
    def deckView(self, deck):
        deckpath = os.path.join(self.defaultDeckPath, deck)
        self.stack_deck_overview.initialize(deckpath, deck)
        
        self.Stack.setCurrentIndex(DECK_OVERVIEW_INDEX)
        
        self.set_tab_text.emit("_view: " + deck)
    
    def createNewDeck(self):
        folder = QFileDialog.getExistingDirectory(self, "SelectDirectory", self.defaultDeckPath)
        if folder:
            self.Stack.setCurrentIndex(DECK_OVERVIEW_INDEX)
            self.stack_deck_overview.initialize(folder, "new deck")
    
    def selectDeck(self):
        self.Stack.setCurrentIndex(SELECT_DECK_INDEX)
        self.stack_language_select.rescanLanguageList()
        
        self.set_tab_text.emit("decks manager")
    
    def createNewDeckItem(self, deckpath, dbAdapter, deckname):
        self.stack_new_deck.setDeckpath(deckpath)
        self.stack_new_deck.setDbAdapter(dbAdapter)
        self.stack_new_deck.initializeAsEmpty(deckname)
        self.Stack.setCurrentIndex(NEW_DECK_INDEX)
        
        self.set_tab_text.emit("create new item: " + deckname)
    
    def editDeckItem(self, deckpath, dbAdapter, rowid, deckname):
        self.stack_new_deck.setDeckpath(deckpath)
        self.stack_new_deck.setDbAdapter(dbAdapter)
        self.stack_new_deck.initializeWithRowID(rowid, deckname)
        self.Stack.setCurrentIndex(NEW_DECK_INDEX)
        
        self.set_tab_text.emit("decks: edit item: " + deckname)
