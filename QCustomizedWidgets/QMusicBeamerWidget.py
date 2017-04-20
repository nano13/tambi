
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

#from QCustomizedWidgets.QDragButton import QDragButton
from QCustomizedWidgets.QScheduleWidget import QScheduleWidget
from QCustomizedWidgets.QBeamerWindow import QBeamerWindow

SCHEDULE_WIDTH = 275

class QMusicBeamerWidget(QWidget):
    
    layout = QHBoxLayout()
    preview_area = None
    
    def __init__(self):
        super().__init__()
        
        self.setLayout(self.layout)
        
        self.schedule = self.addSchedule()
        #self.preview = self.addPreviewArea()
        
        self.addTestDataSet()
        
    def addTestDataSet(self):
        import os
        base, dirs, files = next(iter(os.walk('./amazing_grace')))
        max_i = 0
        for path in sorted(files):
            #label = str(f.split('.')[0])
            print(base, dirs, path)
            self.addScheduleTextFile(base, path)
            
        
        #for i in range(0, 50):
        #    self.addScheduleTextFile(None, None)
        
    def addSchedule(self):
        schedule = QScheduleWidget()
        schedule.button_selected.connect(self.scheduleButtonClicked)
        
        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(schedule)
        scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        
        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth( SCHEDULE_WIDTH )
        scroll_area.setWidget(scroll_widget)
        
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(scroll_area)
        
        return schedule
        
    def addScheduleTextFile(self, basepath, filename):
        label = str(filename.split('.')[0])
        self.schedule.addButton(label)
        
    def scheduleButtonClicked(self, button_id):
        print("CLICK")
        self.addPreviewArea()
    
    def addPreviewArea(self):
        if not self.preview_area == None:
            self.layout.removeWidget(self.preview_area)
        
        preview_widget = QWidget()
        preview_widget.setStyleSheet('QWidget { background-color: yellow; }')
        
        preview_layout = QVBoxLayout()
        preview_widget.setLayout(preview_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(preview_widget)
        
        self.layout.addWidget(scroll_area)
        self.preview_area = scroll_area
        
        self.addPreviewsToPrevievArea()
        
    def addPreviewsToPrevievArea(self):
        test_image = './assets/images/facepalm/facepalm1.jpg'
        print(test_image)
        
        beamer_window = QBeamerWindow()
        
        #beamer_window.hide()
        #beamer_window.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
        #beamer_window.routeToScreen()
        #beamer_window.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
        
        #beamer_window.setImageWithPath(test_image)
        beamer_window.setText('fsdfasdasd')
        beamer_window.routeToScreen()
        #beamer_window.accept()
        #beamer_window.show()
        #beamer_window.raise_()
        #beamer_window.activateWindow()
        #beamer_window.showFullScreen()
        #beamer_window.layout.invalidate()
        #beamer_window.layout.activate()
        #beamer_window.layout.update()
        #beamer_window.exec_()
        
        #desktop = QtWidgets.QApplication.desktop()
        #screen_rect = desktop.screenGeometry(0)
        #beamer_window.paintEvent(QtGui.QPaintEvent(QtCore.QRect(0, 0, screen_rect.width(), screen_rect.height())))
        #beamer_window.repaint()
        
        
        
        preview_pixmap = beamer_window.getPreviewPixmap()
        #preview_pixmap = preview_pixmap.scaled(label.size(), QtCore.Qt.KeepAscpectRatio)
        
        label = QLabel(self)
        label.setGeometry(QtCore.QRect(0, 0, 400, 400))
        label.setPixmap(preview_pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout = self.preview_area.widget().layout()
        layout.addWidget(label)
        
        #beamer_window.destroy()
        
