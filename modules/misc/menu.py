
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

from modules.misc.QAmazingGraceWidget import QAmazingGraceWidget

import functools

class Menu(object):
    def __init__(self, context, menubar):
        
        miscMenu = menubar.addMenu('&Misc')
        
        miscGui = QAction(QIcon.fromTheme("document-properties"), '&Amazing Grace', context)
        miscGui.setStatusTip('Install or Remove Sword Modules')
        misc = QAmazingGraceWidget()
        miscGui.triggered.connect(functools.partial(context.addNewCustomTab, misc, 'amazing grace'))
        
        miscMenu.addAction(miscGui)
