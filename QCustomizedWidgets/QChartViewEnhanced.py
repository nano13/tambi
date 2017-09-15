
from PyQt5.QtChart import QChartView
from PyQt5.QtCore import Qt, QPointF

class QChartViewEnhanced(QChartView):
    
    last_mouse_pos = None
    
    def __init__(self, chart):
        super().__init__()
        
        self.setChart(chart)
    
    def viewportEvent(self, event):
        return super().viewportEvent(event)
    
    def mousePressEvent(self, event):
        button = event.buttons()
        if button == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
        
    
    def mouseMoveEvent(self, event):
        button = event.buttons()
        if button == Qt.LeftButton and self.last_mouse_pos:
            delta_x = self.last_mouse_pos.x() - event.x()
            delta_y = self.last_mouse_pos.y() - event.y()
            
            self.chart().scroll(delta_x, -delta_y)
        
        self.last_mouse_pos = event.pos()
    
    def mouseReleaseEvent(self, event):
        return super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event):
        STEP = 20
        
        key = event.key()
        if key == Qt.Key_Left:
            self.chart().scroll(-STEP, 0)
        
        elif key == Qt.Key_Right:
            self.chart().scroll(+STEP, 0)
        
        elif key == Qt.Key_Up:
            self.chart().scroll(0, +STEP)
        
        elif key == Qt.Key_Down:
            self.chart().scroll(0, -STEP)
    
