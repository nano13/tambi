
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QScrollArea
from PyQt5 import QtCore, QtGui
#from PyQt5.QtGui import QIcon
from QCustomizedWidgets.QDragButton import QDragButton

from functools import partial

WIDTH = 250
SCROLLBAR_WIDTH = 15
BUTTON_HEIGHT = 25

class QScheduleWidget(QWidget):
    
    button_selected = QtCore.pyqtSignal(int, str, str)
    button_list = []
    i = 0
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)
        
    def addButton(self, label, basepath, filename):
        self.i += 1
        
        button = QDragButton(str(label), self, basepath, filename)
        button.setButtonList(self.button_list)
        button.setButtonHeight( BUTTON_HEIGHT )
        
        button.left_clicked.connect(self.leftClicked)
        button.right_clicked.connect(self.rightClicked)
        button.drag_event_ended.connect(self.reorganize)
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.delete_triggered.connect(self.removeButton)
        
        button.setFixedWidth( WIDTH - SCROLLBAR_WIDTH )
        button.setFixedHeight( BUTTON_HEIGHT )
        
        button.move(0, len(self.button_list) * BUTTON_HEIGHT)
        button.button_id = self.i
        
        self.button_list.append(button)
        button.show()
        
        self.setFixedHeight( len(self.button_list) * BUTTON_HEIGHT + 2*BUTTON_HEIGHT )
        
        
    def removeButton(self, button):
        for i, item in enumerate(self.button_list):
            if item == button:
                item.hide()
                del self.button_list[i]
                self.reorganize()
    
    def removeAllButtons(self, bla):
        while len(self.button_list) > 0:
            button = self.button_list.pop(0)
            button.hide()
        
    def leftClicked(self, button_id, basepath, filename):
        print(button_id, basepath, filename)
        self.button_selected.emit(button_id, basepath, filename)
        
    def rightClicked(self, button):
        pass
    
    def reorganize(self):
        self.bubblesortButtons()
        
        i = -1
        for button in self.button_list:
            i += 1
            
            button.move(0, i*BUTTON_HEIGHT)
            
    def bubblesortButtons(self):
        i = -1
        while i < len(self.button_list)-2:
            i += 1
            
            if self.button_list[i].y() > self.button_list[i+1].y():
                self.button_list[i], self.button_list[i+1] = self.button_list[i+1], self.button_list[i]
                
                i = -1
