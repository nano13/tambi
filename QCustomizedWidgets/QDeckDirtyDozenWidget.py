
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

from QCustomizedWidgets.QClickLabel import QClickLabel

from misc.deckDbAdapter import DeckDbAdapter

from os import path
import functools
from random import randint

COLUMNS = 4
DISPLAY_COMBO_ITEMS = ['image', 'name', 'word', 'translation']

class QDeckDirtyDozenWidget(QWidget):
    
    deckpath = None
    
    grid = None
    
    selectDeck = pyqtSignal()
    
    audio_data = None
    audioPlayer = None
    
    curent_audio_deck_id = None
    
    last_random_audio = None
    
    """ holds one of DISPLAY_COMBO_ITEMS: """
    test_mode = 'image'
    
    def __init__(self):
        super().__init__()
        
    def initialize(self, deckpath):
        self.deckpath = deckpath
        
        self.clear()
        
        self.audioPlayer = QMediaPlayer()
        
        db_path = path.join(deckpath, "database.sqlite")
        self.dbAdapter = DeckDbAdapter()
        self.dbAdapter.initialize(db_path)
        dataset = self.dbAdapter.selectDeckDirtyDozenItems()
        self.audio_data = self.dbAdapter.selectAudio()
        
        deck_select_button = QPushButton("<<<")
        deck_select_button.clicked.connect(self.selectDeckButtonClicked)
        
        replay_audio_button = QPushButton("replay audio")
        replay_audio_button.setIcon(QIcon.fromTheme('media-playback-start'))
        replay_audio_button.clicked.connect(self.replayAudioClicked)
        
        select_display_combo_label = QLabel('select display:')
        select_display_combo_label.setAlignment(QtCore.Qt.AlignRight)
        select_display_combo = QComboBox()
        select_display_combo.addItems(DISPLAY_COMBO_ITEMS)
        select_display_combo.setCurrentIndex(DISPLAY_COMBO_ITEMS.index(self.test_mode))
        select_display_combo.currentIndexChanged.connect(self.selectDisplayCurrentIndexChanged)
        
        if not self.layout():
            self.grid = QGridLayout()
            self.grid.setContentsMargins(0, 0, 0, 0)
        
        self.grid.addWidget(deck_select_button, 0, 0)
        self.grid.addWidget(select_display_combo_label, 0, 1)
        self.grid.addWidget(select_display_combo, 0, 2)
        self.grid.addWidget(replay_audio_button, 0, 3)
        
        for i, value in enumerate(dataset, COLUMNS):
            label = QClickLabel()
            if self.test_mode == 'image':
                preview_pixmap = QPixmap()
                try:
                    preview_pixmap.load(path.join(deckpath, value["image"]))
                except (KeyError, TypeError):
                    try:
                        preview_pixmap.load(path.join(deckpath, value["svg_filename"]))
                    except (KeyError, TypeError):
                        pass
                scaled_pixmap = preview_pixmap.scaled(QtCore.QSize(200, 200), QtCore.Qt.KeepAspectRatio)
                label.setGeometry(scaled_pixmap.rect())
                label.setPixmap(scaled_pixmap)
            elif self.test_mode == 'name':
                label.setText(value['name'])
            elif self.test_mode == 'word':
                label.setText(value['word'])
            elif self.test_mode == 'translation':
                label.setText(value['translation'])
            
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.clicked.connect(functools.partial(self.labelClicked, value["rowid"]))
            
            self.grid.addWidget(label, int(i / COLUMNS), i % COLUMNS)
        
        self.setLayout(self.grid)
        
        self.playRandomAudio()
    
    def clear(self):
        if self.grid:
            for i in range(0, self.layout().count()):
                widget = self.layout().itemAt(i).widget()
                widget.setVisible(False)
        #for widget in self.findChildren:
            #print(widget)
        #if self.grid:
            ## just reparent the layout to a temporary one for delete it
            #QWidget().setLayout(self.grid)
    
    def selectDeckButtonClicked(self):
        self.selectDeck.emit()
    
    def labelClicked(self, row_id):
        try:
            if row_id == self.current_audio_deck_id:
                self.playRandomAudio()
        except AttributeError:
            """ we probably have no audio file in this module """
            pass
        
    def playRandomAudio(self):
        try:
            selector = randint(0, len(self.audio_data)-1)
            depth = 0
            while selector == self.last_random_audio:
                selector = randint(0, len(self.audio_data)-1)
                """ to avoid ininite loops with just one element """
                depth += 1
                if depth > 20:
                    break
            self.last_random_audio = selector
            
            filename = self.audio_data[selector]["filename"]
            self.current_audio_deck_id = self.audio_data[selector]["deck_rowid"]
            
            filepath = path.join(self.deckpath, filename)
            url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filepath).absoluteFilePath())
            content = QMediaContent(url)
            self.audioPlayer.setMedia(content)
            self.audioPlayer.play()
        except ValueError:
            """ probably an empty deck. just do nothing"""
            pass
    
    def replayAudioClicked(self):
        self.audioPlayer.play()
    
    def selectDisplayCurrentIndexChanged(self, test):
        selected_label = DISPLAY_COMBO_ITEMS[test]
        self.clear()
        self.test_mode = selected_label
        
        self.initialize(self.deckpath)
