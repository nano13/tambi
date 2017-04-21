 
from PyQt5 import QtCore, QtGui, QtWidgets


class QDragButton(QtWidgets.QPushButton):
    
    drag_event_ended = QtCore.pyqtSignal()
    left_clicked = QtCore.pyqtSignal(int, str, str)
    right_clicked = QtCore.pyqtSignal(QtWidgets.QPushButton)
    
    button_id = -1
    
    basepath = None
    filename = None
    
    #def __init__(self, label, context):
    #    super().__init__(label, context)
        
    def __init__(self, label, context, basepath, filename):
        super().__init__(label, context)
        self.basepath = basepath
        self.filename = filename
    
    def setButtonList(self, button_list):
        self.button_list = button_list
    def setButtonHeight(self, button_height):
        self.button_height = button_height
    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        elif event.button() == QtCore.Qt.RightButton:
            self.right_clicked.emit(self)
        
        super(QDragButton, self).mousePressEvent(event)
        
        self.last_pos = self.y()
    
    def mouseMoveEvent(self, event):
        
        if event.buttons() == QtCore.Qt.LeftButton:
            # nur wenn der bewegte abstand eine bestimmte differenz ueberschreitet:
            
                self.raise_()
                
                # adjust offset from clicked point to origin of widget
                currPos = self.mapToGlobal(self.pos())
                globalPos = event.globalPos()
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                
                if newPos.y() < (self.button_height * len(self.button_list)):
                    if newPos.y() > 0 - self.button_height / 2:
                        self.move( QtCore.QPoint(0, newPos.y()) )
                
                #print(newPos.y())
                
                self.__mouseMovePos = globalPos
        
        super(QDragButton, self).mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.drag_event_ended.emit()
        
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
            
        if event.button() == QtCore.Qt.LeftButton:
            self.left_clicked.emit(self.button_id, self.basepath, self.filename)
        
        super(QDragButton, self).mouseReleaseEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = QtWidgets.QWidget()
    w.resize(800,600)
    
    button = QDragButton("Drag", w)
    #button.clicked.connect(clicked)
    
    w.show()
    app.exec_() 
