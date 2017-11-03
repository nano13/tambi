
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from modules.deck.QGui.QDeckStackedWidget import QDeckStackedWidget

import functools

class Menu(object):
    def __init__(self, context, menubar):
        
        deckMenu = menubar.addMenu('&Deck')
        
        decksManagerAction = QAction(QIcon.fromTheme("document-properties"), '&Decks Manager', context)
        decksManagerAction.setStatusTip('See an Overview of all Decks / edit / create Decks')
        decksManagerAction.triggered.connect(functools.partial(self.addDecksManagerTab, context))
        
        deckMenu.addAction(decksManagerAction)
    
    def addDecksManagerTab(self, context):
        decks_widget = QDeckStackedWidget().deckWidget()
        context.addNewCustomTab(decks_widget, 'decks manager')
