
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from modules.sword.sword import Sword
from modules.sword.QGui.QSwordGui import QSwordGui
from modules.sword.QGui.QParallelBibleWidget import QParallelBibleWidget
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
        swordGuiAction.triggered.connect(functools.partial(self.addSwordGuiTab, context))
        
        swordMenu.addAction(swordGuiAction)
        
        swordParallelViewAction = QAction(QIcon.fromTheme("document-properties"), '&Parallel Bible View', context)
        swordParallelViewAction.setStatusTip('Compare multiple bible translations')
        swordParallelViewAction.triggered.connect(functools.partial(self.addParallelViewTab, context))
        
        swordMenu.addAction(swordParallelViewAction)
        
        swordMenu.addSeparator()
        
        moduleManagerAction = QAction(QIcon.fromTheme("document-properties"), '&Module Manager', context)
        moduleManagerAction.setStatusTip('Install or Remove Sword Modules')
        moduleManagerAction.triggered.connect(functools.partial(self.addSwommTab, context))
        
        swordMenu.addAction(moduleManagerAction)
    
    def addSwordGuiTab(self, context):
        sword_gui = QSwordGui()
        context.addNewCustomTab(sword_gui, 'sword gui')
    
    def addParallelViewTab(self, context):
        parallel_gui = QParallelBibleWidget()
        context.addNewCustomTab(parallel_gui, 'parallel bible gui')
    
    def addSwommTab(self, context):
        swomm = QSwordModuleManager()
        context.addNewCustomTab(swomm, 'sword module manager')
