
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout, QWidget, QGraphicsEllipseItem
from PyQt5.QtGui import QPen, QPainter
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class QMapView(QGraphicsView):
    
    #SCALE_FACTOR = 1000000000
    #PEN_RADIUS = 100000
    SCALE_FACTOR = 10000
    PEN_RADIUS = 100000
    COLOUR = QtCore.Qt.darkGreen
    
    def __init__(self):
        super().__init__()
        
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
    
    def addPoint(self, point_x, point_y):
        point_x, point_y = point_x*self.SCALE_FACTOR, point_y*self.SCALE_FACTOR
        
        pos = QtCore.QPointF(self.mapToScene(point_x, point_y*-1))
        ellipseItem = QGraphicsEllipseItem(pos.x(), pos.y(), self.PEN_RADIUS, self.PEN_RADIUS)
        ellipseItem.setPen(QPen(self.COLOUR, QtCore.Qt.SolidPattern))
        ellipseItem.setBrush(self.COLOUR)
        
        self.scene().addItem(ellipseItem)
    
    def scaleViewToContents(self):
        bounds = self.scene().itemsBoundingRect()
        self.fitInView(bounds, Qt.KeepAspectRatio)
        

from PyQt5.QtWidgets import QMainWindow

class QMapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.resize(500, 500)
        
        grid = QGridLayout()
        
        mapView = QMapView()
        grid.addWidget(mapView, 0, 0)
        
        self.setCentralWidget(mapView)
        
    
    
if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    c = QMapWindow()
    c.show()
    sys.exit(app.exec_())
