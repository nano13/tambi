
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTextEdit, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

class QItemizedWidget(QWidget):
    def __init__(self, payload):
        super().__init__()
        
        #container widget
        widget = QWidget()
        #layout of container widget
        self.layout = QVBoxLayout(self)
        self.showData(payload)
        widget.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        #scroll area properties
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        
        #scroll area layer add
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)
    
    def showData(self, payload):
        for line in payload:
            self.layout.addWidget(QItemWidget(line))
            
    
class QItemWidget(QWidget):
    def __init__(self, line):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.showData(line)
    
    def showData(self, line):
        for column in line:
            text_edit = QGrowingTextEdit()
            text_edit.setText(str(column))
            text_edit.setObjectName("bla")
            text_edit.setReadOnly(True)
            self.layout.addWidget(text_edit)

class QGrowingTextEdit(QTextEdit):
    
    resize = pyqtSignal(name='resize')
    
    def __init__(self):
        super().__init__()
        
        self.document().contentsChanged.connect(self.sizeChange)
        self.cursorPositionChanged.connect(self.sizeChange)
        self.textChanged.connect(self.sizeChange)
        self.resize.connect(self.sizeChange)
        QTimer.singleShot(1, self.sizeChange)
        
        self.heightMin = 0
        self.heightMax = 65000
        
    def resizeEvent(self, e):
        self.sizeChange()
        super().resizeEvent(e)
    
    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight+2)
    
