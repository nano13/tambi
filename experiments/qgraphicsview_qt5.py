

from PyQt5.QtWidgets import QWidget, QGraphicsView, QApplication, QGraphicsScene, QPushButton, QVBoxLayout, QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem
from PyQt5 import QtCore
from PyQt5.QtGui import QPen, QCursor, QPixmap

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.view = View(self)
        self.button = QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def handleClearView(self):
        self.view.scene().clear()

class View(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        
        self.penRadius = 5
        self.rubberRadius = 10
        
        self.mouseButton = None
        self.lastMousePos = None

    def mousePressEvent(self, event):
        
        if event.button() == QtCore.Qt.LeftButton:
            self.mouseButton = QtCore.Qt.LeftButton
            
            self._start = event.pos()
            self.lastMousePos = event.pos()
            
            pos = QtCore.QPointF(self.mapToScene(event.pos()))
            ellipseItem = QGraphicsEllipseItem(pos.x()-(self.penRadius/2), pos.y()-(self.penRadius/2), self.penRadius, self.penRadius)
            ellipseItem.setPen(QPen(QtCore.Qt.green, QtCore.Qt.SolidPattern))
            ellipseItem.setBrush(QtCore.Qt.green)
            
            self.scene().addItem(ellipseItem)
            
        elif event.button() == QtCore.Qt.RightButton:
            self.mouseButton = QtCore.Qt.RightButton
            
            self.eraseWithRubber(event)
            
        self.updateMouseCursor(event)
            
    def updateMouseCursor(self, event):
        
        if self.mouseButton == QtCore.Qt.LeftButton:
            #QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))
            cursor_pixmap = QPixmap("red_cursor.png")
            cursor_pixmap = cursor_pixmap.scaled(self.penRadius, self.penRadius, QtCore.Qt.KeepAspectRatio)
            QApplication.setOverrideCursor(QCursor(cursor_pixmap))
        
        elif self.mouseButton == QtCore.Qt.RightButton:
            #QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))
            cursor_pixmap = QPixmap("red_cursor.png")
            cursor_pixmap = cursor_pixmap.scaled(self.rubberRadius, self.rubberRadius, QtCore.Qt.KeepAspectRatio)
            QApplication.setOverrideCursor(QCursor(cursor_pixmap))
            
    def mouseReleaseEvent(self, event):
        QApplication.restoreOverrideCursor()
        
#    def NOmouseReleaseEvent(self, event):
#        start = QtCore.QPointF(self.mapToScene(self._start))
#        end = QtCore.QPointF(self.mapToScene(event.pos()))
#        self.scene().addItem(
#            QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))
#        for point in (start, end):
#            text = self.scene().addSimpleText(
#                '(%d, %d)' % (point.x(), point.y()))
#            text.setBrush(QtCore.Qt.red)
#            text.setPos(point)
    
    def mouseMoveEvent(self, event):
        
        if self.mouseButton == QtCore.Qt.LeftButton:
            start = QtCore.QPointF(self.mapToScene(self.lastMousePos))
            end = QtCore.QPointF(self.mapToScene(event.pos()))
            
            lineItem = QGraphicsLineItem(QtCore.QLineF(start, end))
            lineItem.setPen(QPen(QtCore.Qt.green, self.penRadius, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
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
        
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
