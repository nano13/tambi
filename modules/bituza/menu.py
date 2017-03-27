
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.bituza.bituza import Bituza

import functools

class Menu(object):
    def __init__(self, context, menubar):
        bituza = Bituza()
        
        bituzaMenu = menubar.addMenu('&Bituza')
