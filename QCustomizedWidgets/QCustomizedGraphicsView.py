
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QTimeLine

class QCustomizedGraphicsView(QGraphicsView):
    
    _numScheduledScalings = 0
    
    def __init__(self):
        super().__init__()
        
        self.setScene(QGraphicsScene(self))
    
    def mousePressEvent(self, event):
        button = event.buttons()
        if button == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
        elif button == Qt.RightButton:
            #print(event.pos())
            print(self.mapToScene(event.pos()))
        """
        elif button == Qt.MidButton:
            mapped = self.mapToScene(event.pos().x(), event.pos().y())
            x = mapped.x()
            y = mapped.y()
            geo = self.convert.convertCanvasToGeo(self.scene_rect, x, y)
            print(geo[0], geo[1])
            print(self.scene().itemsBoundingRect())
        """
    
    def mouseMoveEvent(self, event):
        vert = self.verticalScrollBar().value()
        hor = self.horizontalScrollBar().value()
        
        button = event.buttons()
        if button == Qt.LeftButton and self.last_mouse_pos:
            delta_x = self.last_mouse_pos.x() - event.x()
            new_x = hor + delta_x
            
            delta_y = self.last_mouse_pos.y() - event.y()
            new_y = vert + delta_y
            
            self.horizontalScrollBar().setValue(new_x)
            self.verticalScrollBar().setValue(new_y)
        
        self.last_mouse_pos = event.pos()
    
    def wheelEvent(self, event):
        numDegrees = event.angleDelta() / 8;
        numSteps = numDegrees / 15;
        self._numScheduledScalings += numSteps.y();
        """ if user moved the wheel in another direction, we reset previously scheduled scalings """
        if self._numScheduledScalings * numSteps.y() < 0:
            self._numScheduledScalings = numSteps.y();
        
        anim = QTimeLine(350, self);
        anim.setUpdateInterval(20);
        
        anim.valueChanged.connect(self.scalingTime)
        anim.finished.connect(self.animFinished)
        
        anim.start();
    
    def scalingTime(self, x):
        factor = 1.0 + self._numScheduledScalings / 300.0;
        self.scale(factor, factor)
    
    def animFinished(self):
        if self._numScheduledScalings > 0:
            self._numScheduledScalings -= 1;
        
        else:
            self._numScheduledScalings += 1;
    
