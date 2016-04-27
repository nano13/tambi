

from PyQt5.QtWidgets import QWidget, QGraphicsView, QApplication, QGraphicsScene, QPushButton, QVBoxLayout, QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QPen, QCursor, QPixmap, QPainter

from misc.exportSVG import ExportSVG
from misc.importSVG import ImportSVG

class QFreehandDrawView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        self.setRenderHint(QPainter.Antialiasing)
        
        self.penRadius = 5
        self.rubberRadius = 10
        self.colour = QtCore.Qt.darkGreen
        
        self.mouseButton = None
        self.lastMousePos = None
        
        self.exportSVG = ExportSVG()
        self.importSVG = ImportSVG()
        
        self.setFixedSize(600, 300)

    def mousePressEvent(self, event):
        
        if event.button() == QtCore.Qt.LeftButton:
            self.mouseButton = QtCore.Qt.LeftButton
            
            self._start = event.pos()
            self.lastMousePos = event.pos()
            
            pos = QtCore.QPointF(self.mapToScene(event.pos()))
            ellipseItem = QGraphicsEllipseItem(pos.x()-(self.penRadius/2), pos.y()-(self.penRadius/2), self.penRadius, self.penRadius)
            ellipseItem.setPen(QPen(self.colour, QtCore.Qt.SolidPattern))
            ellipseItem.setBrush(self.colour)
            
            self.scene().addItem(ellipseItem)
            
        elif event.button() == QtCore.Qt.RightButton:
            self.mouseButton = QtCore.Qt.RightButton
            
            self.eraseWithRubber(event)
            
        self.updateMouseCursor(event)
            
    def updateMouseCursor(self, event):
        
        if self.mouseButton == QtCore.Qt.LeftButton:
            #QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))
            cursor_pixmap = QPixmap("images/red_cursor.png")
            cursor_pixmap = cursor_pixmap.scaled(self.penRadius, self.penRadius, QtCore.Qt.KeepAspectRatio)
            QApplication.setOverrideCursor(QCursor(cursor_pixmap))
        
        elif self.mouseButton == QtCore.Qt.RightButton:
            #QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))
            cursor_pixmap = QPixmap("images/red_cursor.png")
            cursor_pixmap = cursor_pixmap.scaled(self.rubberRadius, self.rubberRadius, QtCore.Qt.KeepAspectRatio)
            QApplication.setOverrideCursor(QCursor(cursor_pixmap))
            
    def mouseReleaseEvent(self, event):
        QApplication.restoreOverrideCursor()
    
    def mouseMoveEvent(self, event):
        
        if self.mouseButton == QtCore.Qt.LeftButton:
            start = QtCore.QPointF(self.mapToScene(self.lastMousePos))
            end = QtCore.QPointF(self.mapToScene(event.pos()))
            
            lineItem = QGraphicsLineItem(QtCore.QLineF(start, end))
            lineItem.setPen(QPen(self.colour, self.penRadius, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            self.scene().addItem(lineItem)
            
            self.lastMousePos = event.pos()
            
        elif self.mouseButton == QtCore.Qt.RightButton:
            self.eraseWithRubber(event)
            
    def eraseWithRubber(self, event):
        x = event.pos().x() - self.rubberRadius/2
        y = event.pos().y() - self.rubberRadius/2
        pos = QtCore.QPointF(self.mapToScene(x, y))
        rect = QtCore.QRectF(pos.x(), pos.y(), self.rubberRadius, self.rubberRadius)
        items = self.scene().items(rect, QtCore.Qt.IntersectsItemShape)
        if items:
            for item in items:
                self.scene().removeItem(item)
                
    def clearView(self):
        self.scene().clear()
        
    def saveView(self, outputfilepath):
        self.exportSVG.exportSVG(outputfilepath, self)
        
    def loadView(self, inputfilepath):
        try:
            self.importSVG.importSVG(inputfilepath, self)
        except FileNotFoundError:
            print("ERROR: File not found: ", inputfilepath)
        
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = QFreehandDrawWidget()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
