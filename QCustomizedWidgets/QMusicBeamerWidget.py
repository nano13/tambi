
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

from QCustomizedWidgets.QScheduleWidget import QScheduleWidget
from QCustomizedWidgets.QBeamerWindow import QBeamerWindow
from QCustomizedWidgets.QClickLabel import QClickLabel

from misc.mimetypeAnalyzer import MimetypeAnalyzer

import functools, os

SCHEDULE_WIDTH = 275
PREVIEW_WIDTH = 300

class QMusicBeamerWidget(QWidget):
    
    layout = QHBoxLayout()
    preview_area = None
    
    beamer_window = None
    
    mimetypeAnalyzer = MimetypeAnalyzer()
    
    def __init__(self):
        super().__init__()
        
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.schedule = self.addSchedule()
        #self.preview = self.addPreviewArea()
        
        self.addTestDataSet()
        
    def addTestDataSet(self):
        #self.addToSchedule('./assets/images/facepalm/', 'facepalm1.jpg')
        base, dirs, files = next(iter(os.walk('./assets/images/facepalm')))
        for filename in sorted(files):
            self.addToSchedule(base, filename)
        
        base, dirs, files = next(iter(os.walk('./amazing_grace')))
        max_i = 0
        for filename in sorted(files):
            #label = str(f.split('.')[0])
            #print(base, dirs, filename)
            self.addToSchedule(base, filename)
            
        
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
        
    def addToSchedule(self, basepath, filename):
        label = str(filename.split('.')[0])
        self.schedule.addButton(label, basepath, filename)
        
    def scheduleButtonClicked(self, button_id, basepath, filename):
        self.addPreviewArea(basepath, filename)
    
    def addPreviewArea(self, basepath, filename):
        if not self.preview_area == None:
            self.layout.removeWidget(self.preview_area)
        
        preview_widget = QWidget()
        #preview_widget.setStyleSheet('QWidget { background-color: yellow; }')
        
        preview_layout = QVBoxLayout()
        preview_widget.setLayout(preview_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(preview_widget)
        
        self.layout.addWidget(scroll_area)
        self.preview_area = scroll_area
        
        self.addPreviewsToPrevievArea(basepath, filename)
        
    def addPreviewsToPrevievArea(self, basepath, filename):
        filetype = self.mimetypeAnalyzer.isImageOrText(basepath, filename)
        
        #test_image = './assets/images/facepalm/facepalm1.jpg'
        #print(test_image)
        
        self.beamer_window = QBeamerWindow()
        
        if filetype == 'image':
            self.beamer_window.setImageWithPath(os.path.join(basepath, filename))
        elif filetype == 'text':
            text = ''
            with open(os.path.join(basepath, filename), 'r') as fobj:
                for line in fobj:
                    text += line
            
            self.beamer_window.setText(text)
            self.beamer_window.routeToScreen() # needed for beamer_window.setText()
        
        preview_pixmap = self.beamer_window.getPreviewPixmap()
        scaled_pixmap = preview_pixmap.scaled(QtCore.QSize(PREVIEW_WIDTH, PREVIEW_WIDTH), QtCore.Qt.KeepAspectRatio)
        
        label = QClickLabel()
        label.setGeometry(scaled_pixmap.rect())
        label.setPixmap(scaled_pixmap)
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        label.clicked.connect(functools.partial(self.previewClicked, None))
        
        layout = self.preview_area.widget().layout()
        layout.addWidget(label)
        
    def previewClicked(self, beamer_window):
        self.beamer_window.routeToScreen()
        self.beamer_window.showFullScreen()
        
        
