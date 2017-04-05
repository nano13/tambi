
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.quran.quran import Quran

import functools

class Menu(object):
    def __init__(self, context, menubar): 
        quran = Quran()
        
        quranMenu = menubar.addMenu('&Quran')
        
        
