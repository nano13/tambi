#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QTabWidget, QAction, qApp, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt
from PyQt5 import QtCore

import signal, os
# to make program closeable with ctr-c in terminal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from QCustomizedWidgets.QCoreTab import QCoreTab

class Logos(QMainWindow):
    
    tab_widget = None
    
    meta_key_pressed = False # Windows-Key or Control-Key on Mac
    
    def __init__(self):
        super().__init__()
        
        self.initGUI()
        self.tab_widget = self.initTabs()
        self.addNewCliTab()
        #self.addNewVocableTab()
        
        self.resize(625, 670)
        self.center()
        
        #self.installEventFilter(self)
        #self.tab_widget.installEventFilter(self)
        
    def center(self):
        geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())
    
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            print("KEY EVENT ::::")
            if self.meta_key_pressed and event.key() == Qt.Key_Left:
                print("LEFT ::::")
                self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()-1)
                QMainWindow.event(self, event)
                return True
            elif self.meta_key_pressed and event.key() == Qt.Key_Right:
                print("RIGHT ::::")
                self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()+1)
                QMainWindow.event(self, event)
                return True
            else:
                return QMainWindow.event(self, event)
        else:
            return QMainWindow.event(self, event)
    
    def eventFilter(self, a, event):
        if event.type() == QtCore.QEvent.KeyPress:
            print("eventFilter: keyPress")
            if self.meta_key_pressed and event.key() == Qt.Key_Left:
                print("LEFT", self.tab_widget.currentIndex())
                self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()-1)
                return True
            elif self.meta_key_pressed and event.key() == Qt.Key_Right:
                print("RIGHT", self.tab_widget.currentIndex())
                self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()+1)
                return True
            else:
                return QMainWindow.eventFilter(self, a, event)
        else:
            return QMainWindow.eventFilter(self, a, event)
        #if event.type() == QtCore.QEvent.KeyPress:
            ##print("A")
            #result = self.keyPressEvent(event)
            
            #if result:
                #return True
            #else:
                #return QMainWindow.eventFilter(self, a, event)
        #else:
            ##print("B")
            #return QMainWindow.eventFilter(self, a, event)
    
    def keyPressEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            if event.key() == Qt.Key_W:
                self.closeTab(self.tab_widget.currentIndex())
        if event.key() == Qt.Key_Meta:
            self.meta_key_pressed = True
        elif self.meta_key_pressed and event.key() == Qt.Key_Up:
            print("prev")
            self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()-1)
        elif self.meta_key_pressed and event.key() == Qt.Key_Down:
            print("next")
            self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex()+1)
        else:
            return QMainWindow.keyPressEvent(self, event)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Meta:
            self.meta_key_pressed = False
    
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
        exitAction = QAction(QIcon.fromTheme("application-exit"), "&Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        
        newCliTabAction = QAction(QIcon.fromTheme('utilities-terminal'), '&New Command Line Tab', self)
        newCliTabAction.setShortcut('Ctrl+T')
        newCliTabAction.setStatusTip('Open new CLI Tab')
        newCliTabAction.triggered.connect(self.addNewCliTab)
        
        newVocableTabAction = QAction(QIcon.fromTheme('input-tablet'), '&New Vocable Tab', self)
        newVocableTabAction.setShortcut('Ctrl+L')
        newVocableTabAction.setStatusTip('Open new Vocable Tab')
        newVocableTabAction.triggered.connect(self.addNewVocableTab)
        
        openFileAction = QAction(QIcon.fromTheme('document-open'), '&Open File', self)
        openFileAction.setStatusTip('Open a File')
        openFileAction.setShortcut('Ctrl+O')
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
        tab_widget = QTabWidget()
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(tab_widget)
        
        return tab_widget
        
    def closeTab(self, tab_id):
        self.tab_widget.removeTab(tab_id)
        
    def addNewCliTab(self):
        tab = QCoreTab().cliTab()
        self.tab_widget.addTab(tab, "cli")
        
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)
        
    def addNewVocableTab(self):
        tab = QCoreTab().vocableTab()
        self.tab_widget.addTab(tab, "vocable")
        
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)
    
    def openFile(self):
        home_path = os.path.expanduser('~')
        file_path = QFileDialog.getOpenFileName(self, "Please select File", home_path)
        
        tab = QCoreTab().editorTab(file_path)
        self.tab_widget.addTab(tab, "editor")
        
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = Logos()
    sys.exit(app.exec_())
