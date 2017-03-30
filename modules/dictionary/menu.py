
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.dictionary.dictionary import Dictionary

import functools

class Menu(object):
    def __init__(self, context, menubar):
        dictionary = Dictionary()
        
        dictionaryMenu = menubar.addMenu('&Dictionary')
        
        
