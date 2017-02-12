
from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QLabel, QGridLayout
try:
    from QCustomizedWidgets.QVirtualKeyboardWidget import QVirtualKeyboardWidget
except ImportError:
    from QVirtualKeyboardWidget import QVirtualKeyboardWidget

class QVirtualKeyboardWindow(QMainWindow):
    
    availableHostLayouts = ["qwertz"]
    availableVirtualLayouts = ["german", "greek", "hebrew", "arabic", "hindi"]
    
    def __init__(self):
        super().__init__()
        
        self.resize(450, 185)
        
        self.virtualKeyboard = QVirtualKeyboardWidget()
        self.virtualKeyboard.drawKeyboard("qwertz", "arabic")
        
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        #grid.setSpacing(0)
        
        layoutHostLabel = QLabel("Host Layout:")
        layoutVirtualLabel = QLabel("Virtual Layout:")
        
        hostLayoutCombo = QComboBox(self)
        for layout in sorted(self.availableHostLayouts):
            hostLayoutCombo.addItem(layout)
        hostLayoutCombo.activated[str].connect(self.onHostLayoutActivated)
        
        virtualLayoutCombo = QComboBox(self)
        for layout in sorted(self.availableVirtualLayouts):
            virtualLayoutCombo.addItem(layout)
        virtualLayoutCombo.activated[str].connect(self.onVirtualLayoutActivated)
        
        grid.addWidget(hostLayoutCombo, 0, 1)
        grid.addWidget(virtualLayoutCombo, 0, 2)
        grid.addWidget(self.virtualKeyboard, 1, 1, 1, 2)
        
        #self.setLayout(grid)
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        
        self.show()
        
    def onHostLayoutActivated(self, layout):
        print(layout)
    
    def onVirtualLayoutActivated(self, layout):
        self.virtualKeyboard.destroyKeyboard()
        self.virtualKeyboard.drawKeyboard("qwertz", layout)
        
    def setLineEdit(self, lineEdit):
        self.virtualKeyboard.setLineEdit(lineEdit)
        pass
        
if __name__ == "__main__":
    import signal
    # to make program closeable with ctr-c in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    c = QVirtualKeyboardWindow()
    sys.exit(app.exec_())
