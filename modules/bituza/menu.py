
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.bituza.bituza import Bituza

import functools

class Menu(object):
    def __init__(self, context, menubar):
        bituza = Bituza()
        
        bituzaMenu = menubar.addMenu('&Bituza')
        
        interlinear = bituzaMenu.addMenu(QIcon.fromTheme("x-office-address-book"), 'interlinear')
        bibles = bituza.structure('', [])
        for book in bibles.payload:
            bookMenu = interlinear.addMenu(QIcon.fromTheme("x-office-address-book"), book[2])
            
            for i in range(book[3]):
                chapterAction = QAction(QIcon.fromTheme("text-x-generic"), str(i+1), context)
                bookMenu.addAction(chapterAction)
                
                chapterAction.triggered.connect(functools.partial(context.addNewCliTabWithCommand, 'bituza.word "'+book[2]+'" '+str(i+1)))
                
