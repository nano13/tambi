
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout

class QBloodlineWidget(QWidget):
    def __init__(self, payload):
        super().__init__()
        
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        
        self.view.setScene(self.scene)
        
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        
        self.setLayout(layout)
    

from PyQt5.QtWidgets import QGraphicsItem

class QGraphicsGuyItem(QGraphicsItem):
    def __init__(self):
        super().__init__()
        
        
