
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.sword.sword import Sword

import functools

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
            languageMenu = biblesMenu.addMenu(QIcon.fromTheme("accessories-dictionary"), lang)
            
            for bible in bibles.payload:
                if bible[1] == lang:
                    bibleAction = QAction(QIcon.fromTheme("x-office-address-book"), bible[0], context)
                    languageMenu.addAction(bibleAction)
                    
                    bibleAction.triggered.connect(functools.partial(context.addNewCliTabWithCommand, 'sword.setModule "'+bible[0]+'"'))
            
        
        books = sword.canons()
        booksMenu = swordMenu.addMenu('books')
        for i, book in enumerate(books):
            bookMenu = booksMenu.addMenu(QIcon.fromTheme("x-office-address-book"), book[0])
            
            for j, chapter in enumerate(books[i][3]):
                chapterAction = QAction(QIcon.fromTheme("text-x-generic"), str(j+1), context)
                bookMenu.addAction(chapterAction)
                
                chapterAction.triggered.connect(functools.partial(context.addNewCliTabWithCommand, 'sword.word "'+book[0]+'" '+str(j+1)))
