
from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QLabel, QGridLayout
from PyQt5 import QtCore
try:
    from QCustomizedWidgets.QVirtualKeyboardWidget import QVirtualKeyboardWidget
except ImportError:
    from QVirtualKeyboardWidget import QVirtualKeyboardWidget

from configs.configFiles import ConfigFile

class QVirtualKeyboardWindow(QMainWindow):
    
    availableHostLayouts = ["qwertz"]
    availableVirtualLayouts = ["german", "greek", "hebrew", "arabic", "hindi", "futhark", "ipa"]
    
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
        hostLayoutCombo.installEventFilter(self)
        
        virtualLayoutCombo = QComboBox(self)
        for layout in sorted(self.availableVirtualLayouts):
            virtualLayoutCombo.addItem(layout)
        virtualLayoutCombo.activated[str].connect(self.onVirtualLayoutActivated)
        virtualLayoutCombo.installEventFilter(self)
        
        grid.addWidget(hostLayoutCombo, 0, 1)
        grid.addWidget(virtualLayoutCombo, 0, 2)
        grid.addWidget(self.virtualKeyboard, 1, 1, 1, 2)
        
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        
        self.applyStylesheet()
        
        self.show()
        
    def applyStylesheet(self):
        config = ConfigFile()
        path = config.readVar('global', 'stylesheet')
        stylesheet = ''
        try:
            with open(path) as css:
                for line in css:
                    stylesheet += line
            
            self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            pass
        
    def onHostLayoutActivated(self, layout):
        print(layout)
    
    def onVirtualLayoutActivated(self, layout):
        self.virtualKeyboard.destroyKeyboard()
        self.virtualKeyboard.drawKeyboard("qwertz", layout)
        
    def setLineEdit(self, lineEdit):
        self.virtualKeyboard.setLineEdit(lineEdit)
        
    def eventFilter(self, a, event):
        if event.type() == QtCore.QEvent.KeyPress:
            self.virtualKeyboard.keyPressEvent(event)
            return True
        
        return False
        
if __name__ == "__main__":
    import signal
    # to make program closeable with ctr-c in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    c = QVirtualKeyboardWindow()
    sys.exit(app.exec_())
