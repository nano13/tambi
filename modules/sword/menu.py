
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.sword.sword import Sword

class Menu(object):
    def __init__(self, context, menubar):
        sword = Sword()
        
        swordMenu = menubar.addMenu('&Sword')
        
        bibles = sword.listModules('', [])
        biblesMenu = swordMenu.addMenu('bibles')
        languages = []
        for bible in bibles.payload:
            if not bible[1] in languages:
                languages.append(bible[1])
        languages.sort()
        
        for lang in languages:
            languageMenu = biblesMenu.addMenu(QIcon.fromTheme("application-exit"), lang)
            
            for bible in bibles.payload:
                if bible[1] == lang:
                    bibleAction = QAction(QIcon.fromTheme("application-exit"), bible[0], context)
                    languageMenu.addAction(bibleAction)
            
        
        books = sword.books('', [])
        booksMenu = swordMenu.addMenu('books')
        for book in books.payload:
            bookAction = QAction(QIcon.fromTheme("application-exit"), book, context)
            booksMenu.addAction(bookAction)
        
        
