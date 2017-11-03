
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from os import path

from functools import partial

class QAudioItems(object):
    
    PLAYING = 1
    STOPPED = 0
    
    audioPlayer = None
    status = STOPPED
    row = None
    
    #max_button_count = 0
    col_offset = 0
    
    def __init__(self, deckpath, tableWidget, max_audio_count, offset):
        self.deckpath = deckpath
        self.tableWidget = tableWidget
        self.tableWidget.setColumnCount(max_audio_count + offset)
        self.col_offset = offset
        
        self.audioPlayer = QMediaPlayer()
        self.audioPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)
        
    def appendPlayButtonsDict(self, audio_filenames, row):
        #if len(audio_filenames) > self.max_button_count:
            ##self.max_button_count = len(audio_filenames) + col_offset
            #self.max_button_count = max_audio_count + col_offset
        #if self.tableWidget.columnCount() < self.max_button_count:
            #self.tableWidget.setColumnCount(self.max_button_count)
        
        for i, audio in enumerate(audio_filenames):
            filename = audio["filename"]
            self.appendPlayButtonsHelper(row, i, filename)
            
    def appendPlayButtonsHelper(self, row, i, filename):
            button_play = QPushButton()
            icon = QIcon.fromTheme('media-playback-start')
            button_play.setIcon(icon)
            button_play.clicked.connect(partial(self.playButtonClicked, filename, row))
            
            #button_play.resize(30, 30)
            
            self.tableWidget.setCellWidget(row, i+self.col_offset, button_play)
    
    def appendPlayButtonsList(self, audio_filenames, row):
        for i, filename in enumerate(audio_filenames):
            self.appendPlayButtonsHelper(row, i, filename)
    
    def playButtonClicked(self, filename, row):
        filepath = path.join(self.deckpath, filename)
        url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filepath).absoluteFilePath())
        content = QMediaContent(url)
        self.audioPlayer.setMedia(content)
        self.audioPlayer.play()
        
        self.status = self.PLAYING
        self.row = row
    
    def stopAllSounds(self):
        self.audioPlayer.stop()
    
    def mediaStatusChanged(self):
        pass
    
    #def getMaxColCount(self):
        #if not self.max_button_count == 0:
            #return self.max_button_count
        #else:
            #return self.tableWidget.columnCount()
 
