
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from modules.sword.sword import Sword
from modules.sword.QGui.QSwordGui import QSwordGui
from modules.sword.QGui.QSwordModuleManager import QSwordModuleManager

import functools

class Menu(object):
    def __init__(self, context, menubar):
        sword = Sword()
        
        swordMenu = menubar.addMenu('&Sword')
        
        bibles = sword.listModules('', [])
        biblesMenu = swordMenu.addMenu(QIcon.fromTheme("accessories-dictionary"), 'bibles')
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
        
        swordMenu.addSeparator()
        
        books = sword.canons()
        for testament in ['ot', 'nt']:
            booksMenu = swordMenu.addMenu(QIcon.fromTheme("x-office-address-book"), 'bible '+testament)
            
            for i, book in enumerate(books[testament]):
                bookMenu = booksMenu.addMenu(QIcon.fromTheme("x-office-address-book"), book[0])
                
                for j, chapter in enumerate(books[testament][i][3]):
                    chapterAction = QAction(QIcon.fromTheme("text-x-generic"), str(j+1), context)
                    bookMenu.addAction(chapterAction)
                    
                    chapterAction.triggered.connect(functools.partial(context.addNewCliTabWithCommand, 'sword.word "'+book[0]+'" '+str(j+1)))
        
        swordMenu.addSeparator()
        
        swordGuiAction = QAction(QIcon.fromTheme("document-properties"), '&Sword GUI', context)
        swordGuiAction.setStatusTip('Read the bible with a specialized selector gui')
        #swordGuiAction.triggered.connect(context.addNewSwordGuiTab)
        sword_gui = QSwordGui()
        swordGuiAction.triggered.connect(functools.partial(context.addNewCustomTab, sword_gui, 'sword gui'))
        
        swordMenu.addAction(swordGuiAction)
        
        #swordMenu.addSeparator()
        
        moduleManagerAction = QAction(QIcon.fromTheme("document-properties"), '&Module Manager', context)
        moduleManagerAction.setStatusTip('Install or Remove Sword Modules')
        swomm = QSwordModuleManager()
        moduleManagerAction.triggered.connect(functools.partial(context.addNewCustomTab, swomm, 'sword module manager'))
        
        swordMenu.addAction(moduleManagerAction)
