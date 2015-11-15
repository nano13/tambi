#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QTabWidget, QTableWidget

import signal
# to make program closeable with ctr-c in terminal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Logos(QMainWindow):
    
    tab_widget = None
    tabs_list = []
    current_tab = 0
    
    def __init__(self):
        super().__init__()
        
        self.initGUI()
        self.initTabs()
        self.addNewTableTab()
        
    def initGUI(self):
        
        self.statusBar().showMessage('Ready')
        
        screen_rectangle = QDesktopWidget().availableGeometry()
        sx, sy = screen_rectangle.getRect()[2], screen_rectangle.getRect()[3]
        
        self.resize(sx*0.61, sy*0.61)
        
        self.setWindowTitle('logos')
        self.show()
        
    def initTabs(self):
        self.tab_widget = QTabWidget()
        
    def addNewTableTab(self):
        #table_tab = QTableWidget()
        self.tabs_list.append(QTableWidget())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    c = Logos()
    sys.exit(app.exec_())