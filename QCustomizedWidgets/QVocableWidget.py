
from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout, QFileDialog
from QCustomizedWidgets.QVocableLearnPage import QVocableLearnPage
from QCustomizedWidgets.QVocableLanguagePage import QVocableLanguagePage
from QCustomizedWidgets.QDeckOverviewWidget import QDeckOverviewWidget
from QCustomizedWidgets.QNewDeckWidget import QNewDeckWidget

#from os.path import expanduser, join
from os import path

class QVocableWidget(QWidget):
    def __init__(self):
        super().__init__()
        
    def vocableWidget(self):
        self.stack_language_select = QVocableLanguagePage()
        self.stack_language_select.vocableLanguagePage()
        self.stack_language_select.languageSelected.connect(self.languageSelected)
        self.stack_language_select.createNewDeckSignal.connect(self.createnewDeck)
        
        self.stack_vocable_learn = QVocableLearnPage()
        self.stack_vocable_learn.vocableLearnPage()
        self.stack_vocable_learn.selectLanguage.connect(self.selectLanguage)
        
        self.stack_deck_overview = QDeckOverviewWidget()
        self.stack_deck_overview.selectDeck.connect(self.selectDeck)
        self.stack_deck_overview.createNewItem.connect(self.createNewDeckItem)
        
        self.stack_new_deck = QNewDeckWidget()
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
        self.Stack.setCurrentIndex(2)
        
    def languageSelected(self, language):
        self.Stack.setCurrentIndex(1)
        
        self.stack_vocable_learn.getVocableList(language)
        
    def createnewDeck(self):
        defaultpath = path.join(path.expanduser("~"), ".logos_bible")
        folder = QFileDialog.getExistingDirectory(self, "SelectDirectory", defaultpath)
        if folder:
            self.Stack.setCurrentIndex(2)
            self.stack_deck_overview.initializeDeckOverview(folder)
            
    def selectDeck(self):
        self.Stack.setCurrentIndex(0)
    
    def createNewDeckItem(self):
        self.Stack.setCurrentIndex(3)
