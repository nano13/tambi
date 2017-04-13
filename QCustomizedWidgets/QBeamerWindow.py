
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtCore, QtGui, QtWidgets

class QBeamerWindow(QDialog):
    
    def __init__(self):
        super().__init__()
        #super(QBeamerWindow, self).__init__(parent)
        
        self.setStyleSheet('QWidget { background-color: darkgreen; }')
        #self.layout = QtWidgets.QGridLayout()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowSystemMenuHint)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        
        QFontDatabase.addApplicationFont('./assets/fonts/Cyberbit.ttf')
    
    def routeToScreen(self):
        desktop = QtWidgets.QApplication.desktop()
        
        last_screen = desktop.screenCount()
        
        screen_rect = desktop.screenGeometry(last_screen-1)
        
        self.move(screen_rect.left(), screen_rect.top())
        self.showFullScreen()
        
    def setText(self, text):
        label = QLabel(text, self)
        
        font = QtGui.QFont("Cyberbit", 50)
        label.setFont(font)
        label.setStyleSheet('QLabel { color: yellow; }')
        
        
        label.setText(text)
        
        self.layout.addWidget(label, QtCore.Qt.AlignCenter)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        
    def destroy(self):
        self.close()
        
if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    
    c = QBeamerWindow()
    c.routeToScreen()
    
    sys.exit(app.exec_())
