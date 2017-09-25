
from PyQt5.QtWidgets import QGridLayout, QLabel
from PyQt5.QtChart import QChartView, QChart, QLineSeries
from PyQt5.QtCore import Qt, QPointF

class QChartViewEnhanced(QChartView):
    
    last_mouse_pos = None
    
    def __init__(self, chart):
        super().__init__()
        self.setChart(chart)
        
        grid = QGridLayout()
        grid.setRowStretch(0, 10000)
        grid.setColumnStretch(1, 10000)
        self.setLayout(grid)
        
        self.label_mouse_pos = QLabel("[right click/drag on chart to see mouse position]")
        grid.addWidget(self.label_mouse_pos, 1, 2)
        self.label_curve = QLabel("[right click/drag on chart to see f(x)]")
        grid.addWidget(self.label_curve, 1, 0)
    
    def viewportEvent(self, event):
        return super().viewportEvent(event)
    
    def mousePressEvent(self, event):
        button = event.buttons()
        if button == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
        
        elif button == Qt.RightButton:
            self.showPositions(event)
    
    def mouseMoveEvent(self, event):
        button = event.buttons()
        if button == Qt.LeftButton and self.last_mouse_pos:
            delta_x = self.last_mouse_pos.x() - event.x()
            delta_y = self.last_mouse_pos.y() - event.y()
            
            self.chart().scroll(delta_x, -delta_y)
        
        elif button == Qt.RightButton:
            self.showPositions(event)
        
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
    
    def showPositions(self, event):
        series = self.chart().series()[0]
        
        view_coord = self.mapToScene(event.pos())
        chart_item_coord = self.chart().mapFromScene(view_coord)
        value = self.chart().mapToValue(chart_item_coord, series)
        value = self.chart().mapToValue(view_coord, series)
        
        self.label_mouse_pos.setText("cursor: "+str(round(value.x(), 3)) + " | " + str(round(value.y(), 3)))
        self.label_curve.setText("f("+str(series.at(value.x()).x()) + ") = " + str(series.at(value.y()).y()))
