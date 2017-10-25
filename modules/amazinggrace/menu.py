
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.amazinggrace.QAmazingGraceWidget import QAmazingGraceWidget

import functools

class Menu(object):
    def __init__(self, context, menubar):
        
        agMenu = menubar.addMenu('&AG')
        
        agGui = QAction(QIcon.fromTheme("document-properties"), '&Amazing Grace', context)
        agGui.setStatusTip('Install or Remove Sword Modules')
        ag = QAmazingGraceWidget()
        agGui.triggered.connect(functools.partial(context.addNewCustomTab, ag, 'amazing grace'))
        
        agMenu.addAction(agGui)
