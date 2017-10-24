
from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel, QTextEdit

from interpreter.interpreter import Interpreter

from modules.sword.sword import Sword

import queue

class QSwordGui(QWidget):
    
    interpreter = Interpreter()
    queue = queue.Queue()
    
    sword = Sword()
    
    def __init__(self):
        super().__init__()
        
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 6)
        self.setLayout(self.grid)
        
        self.text_edit = QTextEdit()
        
        self.combo_language = QComboBox()
        self.combo_translation = QComboBox()
        self.combo_book = QComboBox()
        self.combo_chapter = QComboBox()
        
        self.combo_language.currentTextChanged.connect(self.languageChanged)
        self.combo_translation.currentTextChanged.connect(self.translationChanged)
        self.combo_book.currentTextChanged.connect(self.bookChanged)
        self.combo_chapter.currentTextChanged.connect(self.chapterChanged)
        
        self.grid.addWidget(QLabel("Language"), 0, 0)
        self.grid.addWidget(QLabel("Translation"), 0, 1)
        self.grid.addWidget(QLabel("Book"), 0, 2)
        self.grid.addWidget(QLabel("Chapter"), 0, 3)
        
        self.grid.addWidget(self.combo_language, 1, 0)
        self.grid.addWidget(self.combo_translation, 1, 1)
        self.grid.addWidget(self.combo_book, 1, 2)
        self.grid.addWidget(self.combo_chapter, 1, 3)
        
        self.grid.addWidget(self.text_edit, 2, 0, 1000, 4)
        
        self.getLanguagesForDropdown()
        self.getBooksForDropdown()
    
    def languageChanged(self, language):
        self.getTranslationsForDropdown(language)
    
    def translationChanged(self, translation):
        self.showText()
    
    def bookChanged(self, book):
        self.getChaptersForDropdown(book)
    
    def chapterChanged(self, chapter):
        self.showText()
    
    def getLanguagesForDropdown(self):
        result = self.interpreter.interpreter('sword.languages', self.queue).payload
        
        self.combo_language.clear()
        self.combo_language.insertItems(0, result)
    
    def getTranslationsForDropdown(self, language):
        result = self.interpreter.interpreter('sword.modules '+language, self.queue).payload
        
        translations = []
        for translation in result:
            translations.append(translation[0])
        
        self.combo_translation.clear()
        self.combo_translation.insertItems(0, translations)
    
    def getBooksForDropdown(self):
        books = self.interpreter.interpreter('sword.books', self.queue).payload
        
        self.combo_book.clear()
        self.combo_book.insertItems(0, books)
    
    def getChaptersForDropdown(self, book):
        books = self.sword.canons()
        
        for testament in books:
            for _b in books[testament]:
                if _b[0] == book:
                    print(_b[3])
                    chapters = []
                    for i, length in enumerate(_b[3]):
                        chapters.append(str(i+1))
                    
                    self.combo_chapter.clear()
                    self.combo_chapter.insertItems(0, chapters)
                    break
            
            # if the inner 'break' was executed, we also want to break the outer loop:
            else:
                continue  # executed if the loop ended normally (no break)
            break  # executed if 'continue' was skipped (break)
    
    def showText(self):
        current_translation = self.interpreter.interpreter('sword.getModule', self.queue).payload
        
        translation = self.combo_translation.currentText()
        book = self.combo_book.currentText()
        chapter = self.combo_chapter.currentText()
        
        if translation:
            self.interpreter.interpreter('sword.setModule '+translation, self.queue)
            text = self.interpreter.interpreter('sword.word "'+book+'" '+chapter, self.queue)
            self.interpreter.interpreter('sword.setModule '+current_translation, self.queue)
            
            self.text_edit.clear()
            self.text_edit.setText(text.toString())
            self.text_edit.setReadOnly(True)
        
