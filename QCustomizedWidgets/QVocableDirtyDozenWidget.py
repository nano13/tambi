
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

from QCustomizedWidgets.QClickLabel import QClickLabel

from misc.deckDbAdapter import DeckDbAdapter

from os import path
import functools
from random import randint

COLUMNS = 4

class QVocableDirtyDozenWidget(QWidget):
    
    deckpath = None
    
    grid = None
    
    selectDeck = pyqtSignal()
    
    audio_data = None
    audioPlayer = None
    
    curent_audio_deck_id = None
    
    def __init__(self):
        super().__init__()
        
    def initialize(self, deckpath):
        self.deckpath = deckpath
        
        self.clear()
        
        self.audioPlayer = QMediaPlayer()
        
        db_path = path.join(deckpath, "database.sqlite")
        self.dbAdapter = DeckDbAdapter()
        self.dbAdapter.initialize(db_path)
        dataset = self.dbAdapter.selectDeckItemsWithImage()
        self.audio_data = self.dbAdapter.selectAudio()
        
        deck_select_button = QPushButton("<<<")
        deck_select_button.clicked.connect(self.selectDeckButtonClicked)
        
        if not self.layout():
            self.grid = QGridLayout()
            self.grid.setContentsMargins(0, 0, 0, 0)
            
        if True:
            self.grid.addWidget(deck_select_button, 0, 0)
            
            for i, datum in enumerate(dataset, COLUMNS):
                preview_pixmap = QPixmap()
                try:
                    preview_pixmap.load(path.join(deckpath, datum["image"]))
                except KeyError:
                    preview_pixmap.load(path.join(deckpath, datum["svg_filename"]))
                
                scaled_pixmap = preview_pixmap.scaled(QtCore.QSize(200, 200), QtCore.Qt.KeepAspectRatio)
                
                label = QClickLabel()
                label.setGeometry(scaled_pixmap.rect())
                label.setPixmap(scaled_pixmap)
                label.setAlignment(QtCore.Qt.AlignCenter)
                
                label.clicked.connect(functools.partial(self.labelClicked, datum["rowid"]))
                
                self.grid.addWidget(label, int(i / COLUMNS), i % COLUMNS)
            
            self.setLayout(self.grid)
        
        self.playRandomAudio()
    
    def clear(self):
        if self.grid:
            for i in range(0, self.layout().count()):
                widget = self.layout().itemAt(i).widget()
                print(widget)
                widget.setVisible(False)
        #for widget in self.findChildren:
            #print(widget)
        #if self.grid:
            ## just reparent the layout to a temporary one for delete it
            #QWidget().setLayout(self.grid)
    
    def selectDeckButtonClicked(self):
        self.selectDeck.emit()
    
    def labelClicked(self, row_id):
        if row_id == self.current_audio_deck_id:
            self.playRandomAudio()
        
    def playRandomAudio(self):
        selector = randint(0, len(self.audio_data)-1)
        print(selector)
        filename = self.audio_data[selector]["filename"]
        self.current_audio_deck_id = self.audio_data[selector]["deck_rowid"]
        
        filepath = path.join(self.deckpath, filename)
        url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filepath).absoluteFilePath())
        content = QMediaContent(url)
        self.audioPlayer.setMedia(content)
        self.audioPlayer.play()
    
    
