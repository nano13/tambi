
from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout
from QCustomizedWidgets.QVocableLearnPage import QVocableLearnPage
from QCustomizedWidgets.QVocableLanguagePage import QVocableLanguagePage

class QVocableWidget(QWidget):
    def __init__(self):
        super().__init__()
        
    def vocableWidget(self):
        self.stack_language_select = QVocableLanguagePage()
        self.stack_language_select.vocableLanguagePage()
        self.stack_language_select.languageSelected.connect(self.languageSelected)
        
        self.stack_vocable_learn = QVocableLearnPage()
        self.stack_vocable_learn.vocableLearnPage()
        self.stack_vocable_learn.selectLanguage.connect(self.selectLanguage)
        
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack_language_select)
        self.Stack.addWidget(self.stack_vocable_learn)
        
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        grid.addWidget(self.Stack)
        
        return self
    
    def displayWidget(self, i):
        self.Stack.setCurrentIndex(0)
        
    def selectLanguage(self):
        self.Stack.setCurrentIndex(0)
        
    def languageSelected(self, language):
        self.Stack.setCurrentIndex(1)
        
        self.stack_vocable_learn.getVocableList(language)
