

from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.view = View(self)
        self.button = QtGui.QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def handleClearView(self):
        self.view.scene().clear()

class View(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        
        self.lastMousePos = None

    def mousePressEvent(self, event):
        self._start = event.pos()
        self.lastMousePos = event.pos()
        
        radius = 10
        
        pos = QtCore.QPointF(self.mapToScene(event.pos()))
        ellipseItem = QtGui.QGraphicsEllipseItem(pos.x()-(radius/2), pos.y()-(radius/2), radius, radius)
        ellipseItem.setPen(QtGui.QPen(QtCore.Qt.green, QtCore.Qt.SolidPattern))
        ellipseItem.setBrush(QtCore.Qt.green)
        
        self.scene().addItem(ellipseItem)
        
        

    def NOmouseReleaseEvent(self, event):
        start = QtCore.QPointF(self.mapToScene(self._start))
        end = QtCore.QPointF(self.mapToScene(event.pos()))
        self.scene().addItem(
            QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))
        for point in (start, end):
            text = self.scene().addSimpleText(
                '(%d, %d)' % (point.x(), point.y()))
            text.setBrush(QtCore.Qt.red)
            text.setPos(point)
            
    def mouseMoveEvent(self, event):
        print(event.pos())
        
        start = QtCore.QPointF(self.mapToScene(self.lastMousePos))
        end = QtCore.QPointF(self.mapToScene(event.pos()))
        
        lineItem = QtGui.QGraphicsLineItem(QtCore.QLineF(start, end))
        lineItem.setPen(QtGui.QPen(QtCore.Qt.green, 10, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        
        self.scene().addItem(lineItem)
        
        self.lastMousePos = event.pos()
        
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
