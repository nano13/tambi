
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtCore, QtGui, QtWidgets

class QBeamerWindow(QDialog):
    
    screen = None
    
    def __init__(self):
        super().__init__()
        
        #self.setStyleSheet('QWidget { background-color: black; }')
        #stylesheet = ''
        #try:
            #with open('/home/samuel/programmierung/logos_bible/assets/css/QTDarkGreen.stylesheet') as css:
                #for line in css:
                    #stylesheet += line
            
            #self.setStyleSheet(stylesheet)
        #except FileNotFoundError:
            #pass
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowSystemMenuHint)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        
        QFontDatabase.addApplicationFont('./assets/fonts/Cyberbit.ttf')
        
    def getScreenRect(self):
        desktop = QtWidgets.QApplication.desktop()
        last_screen = desktop.screenCount()
        self.screen = last_screen-1
        screen_rect = desktop.screenGeometry(self.screen)
        return screen_rect
    
    def routeToScreen(self):
        screen_rect = self.getScreenRect()
        self.move(screen_rect.left(), screen_rect.top())
        #self.showFullScreen()
        
    def setText(self, text):
        label = QLabel(text, self)
        
        font = QtGui.QFont("Cyberbit", 50)
        label.setFont(font)
        label.setStyleSheet('QLabel { color: white; }')
        
        label.setText(text)
        
        self.layout.addWidget(label, QtCore.Qt.AlignCenter)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        
    def setImageWithPixmap(self, pixmap):
        screen_rect = self.getScreenRect()
        rect = QtCore.QRect(0, 0, screen_rect.width(), screen_rect.height())
        
        label = QLabel(self)
        label.setGeometry(rect)
        
        pixmap_scaled = pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
        
        label.setPixmap(pixmap_scaled)
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.layout.addWidget(label, QtCore.Qt.AlignCenter)
        
    def setImageWithPath(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        self.setImageWithPixmap(pixmap)
        
    def setWidget(self, widget):
        self.layout.addWidget(widget)
        
        #self.layout.addWidget(widget, QtCore.Qt.AlignCenter)
        #self.layout.setAlignment(QtCore.Qt.AlignCenter)
    
    def getPreviewImage(self):
        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.screenGeometry(self.screen)
        #rect = QtCore.QRect(0, 0, screen_rect.width(), screen_rect.height())
        
        self.resize(screen_rect.width(), screen_rect.height())
        image = QtGui.QImage(self.size(), QtGui.QImage.Format_ARGB32)
        
        painter = QtGui.QPainter(image)
        
        if painter.isActive():
            self.render(painter)
        else:
            print("Painter Inactive")
        painter.end()
        
        return image
    
    def getPreviewPixmap(self):
        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.screenGeometry(self.screen)
        self.resize(screen_rect.width(), screen_rect.height())
        
        return self.grab()
    
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
