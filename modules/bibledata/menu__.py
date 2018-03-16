
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.bibledata.bibledata import Bibledata

import functools

class Menu(object):
    def __init__(self, context, menubar): 
        bibledata = Bibledata()
        
        bibledataMenu = menubar.addMenu('&BibleData')
        
        
