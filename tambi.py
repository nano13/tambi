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

from QCustomizedWidgets.menuBar import MenuBar
from QCustomizedWidgets.QCoreTab import QCoreTab

from configs.configFiles import ConfigFile

class Tambi(QMainWindow):
    
    tab_widget = None
    
    meta_key_pressed = False # Windows-Key or Control-Key on Mac
    
    config = ConfigFile()
    
    def __init__(self):
        super().__init__()
        
        self.initGUI()
        self.tab_widget = self.initTabs()
        self.addNewCliTab()
        #self.addNewVocableTab()
        #self.addNewMusicWidgetTab()
        #self.addNewSwordModuleManagerTab()
        
        self.resize(825, 670)
        self.center()
        
        #self.installEventFilter(self)
        #self.tab_widget.installEventFilter(self)
        
        QIcon.setThemeSearchPaths(['./assets/icons'])
        
        #for path in QIcon.themeSearchPaths():
        #    print(path, QIcon.themeName())
        QIcon.setThemeName('oxygen')
        print(QIcon.themeName())
        
        if len(sys.argv) > 1:
            if sys.argv[1] == "--quickrun":
                command = sys.argv[2]
                #print(command)
                self.addNewCliTabWithCommand(command)
        
    def center(self):
        geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())
        
    """
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
    """
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
        self.setWindowIcon(QIcon('./assets/icons/logo2.png'))
        
        #self.statusBar().showMessage('Ready')
        
        #screen_rectangle = QDesktopWidget().availableGeometry()
        #sx, sy = screen_rectangle.getRect()[2], screen_rectangle.getRect()[3]
        #
        #self.resize(sx*0.61, sy*0.61)
        
        MenuBar(self)
        
        self.applyStylesheet()
        
        self.setWindowTitle('tambi')
        self.show()
        
    def applyStylesheet(self):
        path = self.config.readVar('global', 'stylesheet')
        stylesheet = ''
        try:
            with open(path) as css:
                for line in css:
                    stylesheet += line
            
            self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            pass
        
    def initTabs(self):
        tab_widget = QTabWidget()
        tab_widget.setTabsClosable(True)
        tab_widget.setMovable(True)
        tab_widget.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(tab_widget)
        
        return tab_widget
        
    def closeTab(self, tab_id):
        self.tab_widget.removeTab(tab_id)
        
    def addNewCliTab(self):
        from functools import partial
        core = QCoreTab()
        #tab = QCoreTab().cliTab()
        tab = core.cliTab()
        self.tab_widget.addTab(tab, "cli")
        
        self.activateNewTab()
        tab.set_tab_text.connect(partial(self.setTabText, self.tab_widget.currentIndex()))
        
    def addNewDualCliTab(self):
        tab = QCoreTab().dualCliTab()
        self.tab_widget.addTab(tab, "dual cli")
        
        self.activateNewTab()
        
    def addNewParallelBibleTab(self):
        tab = QCoreTab().parallelBibleTab()
        self.tab_widget.addTab(tab, "parallel view")
        
        self.activateNewTab()
    
    def setTabText(self, tab_id, text):
        self.tab_widget.setTabText(tab_id, text)
    
    """ to be used internally by the menus """
    def addNewCliTabWithCommand(self, command):
        self.addNewCliTab()
        self.tab_widget.currentWidget().commandEntered(command)
    
    def addNewVocableTab(self):
        tab = QCoreTab().vocableTab()
        self.tab_widget.addTab(tab, "vocable")
        
        self.activateNewTab()
    
    def addNewMusicWidgetTab(self):
        tab = QCoreTab().musicBeamerTab()
        self.tab_widget.addTab(tab, "music beamer")
        
        self.activateNewTab()
    
    def addNewSwordModuleManagerTab(self):
        tab = QCoreTab().swordModuleManagerTab()
        self.tab_widget.addTab(tab, "sword module manager")
        
        self.activateNewTab()
    
    def addNewAmazingGraceTab(self):
        tab = QCoreTab().amazingGraceTab()
        self.tab_widget.addTab(tab, "Amazing Grace")
        
        self.activateNewTab()
    def facepalm(self):
        from QCustomizedWidgets.QBeamerWindow import QBeamerWindow
        self.canvas = QBeamerWindow()
        self.canvas.setImageWithPath('./assets/images/facepalm/facepalm1.jpg')
        self.canvas.routeToScreen()
        self.canvas.showFullScreen()
    
    def openFile(self):
        home_path = os.path.expanduser('~')
        file_path = QFileDialog.getOpenFileName(self, "Please select File", home_path)
        
        print("FILEPATH:", file_path)
        if file_path != ('', ''):
            tab = QCoreTab().editorTab(file_path)
            self.tab_widget.addTab(tab, "editor")
            
            self.activateNewTab()
    
    def activateNewTab(self):
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = Tambi()
    sys.exit(app.exec_())
