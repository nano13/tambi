
from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout, QFileDialog, QMessageBox
from modules.vocable.QGui.QVocableLearnPage import QVocableLearnPage
from modules.vocable.QGui.QVocableLanguagePage import QVocableLanguagePage

from configs.configFiles import ConfigFile

import os

SELECT_LANGUAGE_INDEX = 0
VOCABLE_LEARN_INDEX = 1

class QVocableStackedWidget(QWidget):
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
    
    def vocableWidget(self):
        self.stack_language_select = QVocableLanguagePage()
        self.stack_language_select.setDefaultDeckPath(self.defaultDeckPath)
        self.stack_language_select.vocableLanguagePage()
        self.stack_language_select.languageSelected.connect(self.languageSelected)
        
        self.stack_vocable_learn = QVocableLearnPage()
        self.stack_vocable_learn.initialize()
        self.stack_vocable_learn.selectLanguage.connect(self.selectLanguage)
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack_language_select)
        self.Stack.addWidget(self.stack_vocable_learn)
        
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        layout = self.setLayout(grid)
        
        grid.addWidget(self.Stack)
        
        return self
    
    def displayWidget(self, i):
        self.Stack.setCurrentIndex(SELECT_LANGUAGE_INDEX)
    
    def selectLanguage(self):
        self.Stack.setCurrentIndex(SELECT_LANGUAGE_INDEX)
    
    def languageSelected(self, language):
        self.Stack.setCurrentIndex(VOCABLE_LEARN_INDEX)
        
        self.stack_vocable_learn.getVocableList(language)
    
    def selectDeck(self):
        self.Stack.setCurrentIndex(SELECT_LANGUAGE_INDEX)
        self.stack_language_select.rescanLanguageList()
