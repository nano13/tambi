
from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout, QFileDialog
from QCustomizedWidgets.QVocableLearnPage import QVocableLearnPage
from QCustomizedWidgets.QVocableLanguagePage import QVocableLanguagePage
from QCustomizedWidgets.QDeckOverviewWidget import QDeckOverviewWidget
from QCustomizedWidgets.QNewDeckItemWidget import QNewDeckItemWidget

#from os.path import expanduser, join
from os import path

class QVocableStackedWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.defaultDeckPath = path.join(path.expanduser("~"), ".logos_bible", "decks")
        
    def vocableWidget(self):
        self.stack_language_select = QVocableLanguagePage()
        self.stack_language_select.setDefaultDeckPath(self.defaultDeckPath)
        self.stack_language_select.vocableLanguagePage()
        self.stack_language_select.languageSelected.connect(self.languageSelected)
        self.stack_language_select.deckSelected.connect(self.deckSelected)
        self.stack_language_select.createNewDeckSignal.connect(self.createnewDeck)
        
        self.stack_vocable_learn = QVocableLearnPage()
        self.stack_vocable_learn.vocableLearnPage()
        self.stack_vocable_learn.selectLanguage.connect(self.selectLanguage)
        
        self.stack_deck_overview = QDeckOverviewWidget()
        self.stack_deck_overview.selectDeck.connect(self.selectDeck)
        self.stack_deck_overview.createNewItem.connect(self.createNewDeckItem)
        self.stack_deck_overview.editDeckItem.connect(self.editDeckItem)
        
        self.stack_new_deck = QNewDeckItemWidget()
        self.stack_new_deck.newDeckPage()
        self.stack_new_deck.selectItem.connect(self.selectItem)
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack_language_select)
        self.Stack.addWidget(self.stack_vocable_learn)
        self.Stack.addWidget(self.stack_deck_overview)
        self.Stack.addWidget(self.stack_new_deck)
        
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        grid.addWidget(self.Stack)
        
        return self
    
    def displayWidget(self, i):
        self.Stack.setCurrentIndex(0)
        
    def selectLanguage(self):
        self.Stack.setCurrentIndex(0)
        
    def selectItem(self):
        self.stack_deck_overview.update()
        self.Stack.setCurrentIndex(2)
        
    def languageSelected(self, language):
        self.Stack.setCurrentIndex(1)
        
        self.stack_vocable_learn.getVocableList(language)
        
    def deckSelected(self, deck):
        self.Stack.setCurrentIndex(2)
        
        deckpath = path.join(self.defaultDeckPath, deck)
        self.stack_deck_overview.initializeDeckOverview(deckpath)
        
    def createnewDeck(self):
        folder = QFileDialog.getExistingDirectory(self, "SelectDirectory", self.defaultDeckPath)
        if folder:
            self.Stack.setCurrentIndex(2)
            self.stack_deck_overview.initializeDeckOverview(folder)
            
    def selectDeck(self):
        self.Stack.setCurrentIndex(0)
    
    def createNewDeckItem(self, deckpath, dbAdapter):
        self.stack_new_deck.setDeckpath(deckpath)
        self.stack_new_deck.setDbAdapter(dbAdapter)
        self.stack_new_deck.initializeAsEmpty()
        self.Stack.setCurrentIndex(3)
        
    def editDeckItem(self, deckpath, dbAdapter, rowid):
        self.stack_new_deck.setDeckpath(deckpath)
        self.stack_new_deck.setDbAdapter(dbAdapter)
        self.stack_new_deck.initializeWithRowID(rowid)
        self.Stack.setCurrentIndex(3)
