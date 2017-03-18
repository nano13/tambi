#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QTabWidget, QAction, qApp, QFileDialog
from PyQt5.QtGui import QIcon

import signal, os
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
        self.addNewCliTab()
        #self.addNewVocableTab()
        
        self.resize(625, 670)
        
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
        newCliTabAction.triggered.connect(self.addNewCliTab)
        
        newVocableTabAction = QAction(QIcon.fromTheme('input-tablet'), '&New Vocable Tab', self)
        newVocableTabAction.setStatusTip('Open new Vocable Tab')
        newVocableTabAction.triggered.connect(self.addNewVocableTab)
        
        openFileAction = QAction(QIcon.fromTheme('document-open'), '&Open File', self)
        openFileAction.setStatusTip('Open a File')
        openFileAction.triggered.connect(self.openFile)
        
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newCliTabAction)
        fileMenu.addAction(newVocableTabAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openFileAction)
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
        
    def addNewCliTab(self):
        tab = QCoreTab().cliTab()
        
        self.tabs_list.append(tab)
        self.tab_widget.addTab(tab, "cli")
        
        self.tab_widget.setCurrentIndex(len(self.tabs_list)-1)
        
    def addNewVocableTab(self):
        tab = QCoreTab().vocableTab()
        
        self.tabs_list.append(tab)
        self.tab_widget.addTab(tab, "vocable")
        
        self.tab_widget.setCurrentIndex(len(self.tabs_list)-1)
    
    def openFile(self):
        home_path = os.path.expanduser('~')
        file_path = QFileDialog.getOpenFileName(self, "Please select File", home_path)
        
        tab = QCoreTab().editorTab(file_path)
        
        self.tabs_list.append(tab)
        self.tab_widget.addTab(tab, "editor")
        
        self.tab_widget.setCurrentIndex(len(self.tabs_list)-1)
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    c = Logos()
    sys.exit(app.exec_())
