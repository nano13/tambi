
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

from modules.musicbeamer.QScheduleWidget import QScheduleWidget
from QCustomizedWidgets.QBeamerWindow import QBeamerWindow
from QCustomizedWidgets.QClickLabel import QClickLabel

from misc.mimetypeAnalyzer import MimetypeAnalyzer

import functools, os, codecs

SCHEDULE_WIDTH = 252
PREVIEW_WIDTH = 300

class QMusicBeamerWidget(QWidget):
    
    layout = QHBoxLayout()
    preview_area = None
    
    #beamer_window = None
    
    mimetypeAnalyzer = MimetypeAnalyzer()
    
    def __init__(self):
        super().__init__()
        
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.schedule = self.addSchedule()
        
        self.addAmazingTestDataSet()
        #self.addSongbeamerTestDataSet()
    
    def addAmazingTestDataSet(self):
        base, dirs, files = next(iter(os.walk('./assets/images/facepalm')))
        for filename in sorted(files):
            self.addToSchedule(base, filename)
        
        base, dirs, files = next(iter(os.walk('./modules/misc/amazing_data')))
        max_i = 0
        for filename in sorted(files):
            self.addToSchedule(base, filename)
    
    def addSongbeamerTestDataSet(self):
        base, dirs, files = next(iter(os.walk('/home/samuel/Dropbox/Songbeamer/Songs/logospanoramasong')))
        for filename in sorted(files):
            self.addToSchedule(base, filename)
            print(base, filename)
    
    def addSchedule(self):
        schedule = QScheduleWidget()
        schedule.button_selected.connect(self.scheduleButtonClicked)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth( SCHEDULE_WIDTH )
        scroll_area.setWidget(schedule)
        
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
        
        #self.beamer_window_list = []
        
        if filetype == 'image':
            beamer_window = QBeamerWindow()
            #self.beamer_window_list.append(beamer_window)
            beamer_window.setImageWithPath(os.path.join(basepath, filename))
            
            self.addPreviewsToPrevievAreaHelper(beamer_window)
        
        elif filetype == 'text':
            
            if filename.endswith('.sng'):
                data = self.parseSNGFile(os.path.join(basepath, filename))
            else:
                text = ''
                try:
                    with open(os.path.join(basepath, filename), 'r') as fobj:
                        for line in fobj:
                            text += line
                except UnicodeDecodeError:
                    with codecs.open(os.path.join(basepath, filename), 'r', 'iso-8859-15') as fobj:
                        for line in fobj:
                            text += line
                data = {0: text}
            
            for page in data.keys():
                page = data[page]
                
                beamer_window = QBeamerWindow()
                #self.beamer_window_list.append(beamer_window)
                
                beamer_window.setText(page)
                beamer_window.routeToScreen()
                
                self.addPreviewsToPrevievAreaHelper(beamer_window)
    
    def addPreviewsToPrevievAreaHelper(self, beamer_window):
        preview_pixmap = beamer_window.getPreviewPixmap()
        scaled_pixmap = preview_pixmap.scaled(QtCore.QSize(PREVIEW_WIDTH, PREVIEW_WIDTH), QtCore.Qt.KeepAspectRatio)
        
        label = QClickLabel()
        label.setGeometry(scaled_pixmap.rect())
        label.setPixmap(scaled_pixmap)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.clicked.connect(functools.partial(self.previewClicked, beamer_window))
        
        layout = self.preview_area.widget().layout()
        layout.addWidget(label)
    
    def previewClicked(self, beamer_window):
        beamer_window.routeToScreen()
        beamer_window.showFullScreen()
    
    def parseSNGFile(self, filepath):
        try:
            with open(filepath, 'r') as fobj:
                return self.sngParserHelper(fobj)
        except UnicodeDecodeError:
            with codecs.open(filepath, 'r', 'iso-8859-15') as fobj:
                return self.sngParserHelper(fobj)
    
    def sngParserHelper(self, fobj):
        result = {}
        text = ''
        
        newline_counter = 0
        for line in fobj:
            if line.startswith('--'):
                newline_counter += 1
                
                result[newline_counter] = text
                
                text = ''
            
            else:
                text += line
        
        return result
    
