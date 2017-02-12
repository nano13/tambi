#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QTabWidget, QAction, qApp
from PyQt5.QtGui import QIcon

import signal
# to make program closeable with ctr-c in terminal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from QCustomizedWidgets.QCoreTab import QCoreTab

class Logos(QMainWindow):
    
    tab_widget = None
    tabs_list = []
    current_tab = 0
    
    def __init__(self):
        super().__init__()
        
        self.initGUI()
        self.initTabs()
        self.addNewTableTab()
        #self.addNewVocableLearnTab()
        #self.addNewVocableLanguageTab()
        self.addNewVocableTab()
        
    def initGUI(self):
        
        self.statusBar().showMessage('Ready')
        
        #screen_rectangle = QDesktopWidget().availableGeometry()
        #sx, sy = screen_rectangle.getRect()[2], screen_rectangle.getRect()[3]
        #
        #self.resize(sx*0.61, sy*0.61)
        self.initMenuBar()
        
        self.setWindowTitle('logos')
        self.show()
        
    def initMenuBar(self):
        #exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction = QAction(QIcon.fromTheme("application-exit"), "&Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        
        newCliTabAction = QAction(QIcon.fromTheme('utilities-terminal'), '&New Command Line Tab', self)
        newCliTabAction.setStatusTip('Open new CLI Tab')
        newCliTabAction.triggered.connect(self.addNewTableTab)
        
        newVocableTabAction = QAction(QIcon.fromTheme('input-tablet'), '&New Vocable Tab', self)
        newVocableTabAction.setStatusTip('Open new Vocable Tab')
        newVocableTabAction.triggered.connect(self.addNewVocableTab)
        
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newCliTabAction)
        fileMenu.addAction(newVocableTabAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        
    def initTabs(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tab_widget)
        
    def closeTab(self, id):
        self.tab_widget.removeTab(id)
        del self.tabs_list[id]
        
    def addNewTableTab(self):
        tab = QCoreTab().tableTab()
        
        self.tabs_list.append(tab)
        self.tab_widget.addTab(tab, "Tab")
        
    #def addNewVocableLearnTab(self):
        #tab = QCoreTab().vocableLearnTab()
        
        #self.tabs_list.append(tab)
        #self.tab_widget.addTab(tab, "VocableLearnTab")
    
    #def addNewVocableLanguageTab(self):
        #tab = QCoreTab().vocableLanguageTab()
        
        #self.tabs_list.append(tab)
        #self.tab_widget.addTab(tab, "VocableLanguageTab")
        
    def addNewVocableTab(self):
        tab = QCoreTab().vocableTab()
        
        self.tabs_list.append(tab)
        self.tab_widget.addTab(tab, "VocableTab")
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    c = Logos()
    sys.exit(app.exec_())
