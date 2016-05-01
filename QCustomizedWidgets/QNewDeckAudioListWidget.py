
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore

from misc.audioRecording import RecordAudio
from QCustomizedWidgets.QDeckAudioItemWidget import QDeckAudioItemWidget

from functools import partial
from os import path

PLAY_BUTTON_COLUMN = 1
RECORD_BUTTON_COLUMN = 1
DELETE_BUTTON_COLUMN = 2

class QNewDeckAudioListWidget(QTableWidget):
    
    deckpath = None
    current_deck_rowid = None
    dbAdapter = None
    
    audioItemsDict = []
    audioPlayer = None
    
    STOPPED = 0
    RECORDING = 1
    PLAYING = 2
    status = 0
    row = None
    
    def __init__(self):
        super().__init__()
        
    def initAudioListWidget(self, dbAdapter, deckpath, current_rowid):
        self.dbAdapter = dbAdapter
        self.deckpath = deckpath
        self.current_deck_rowid = current_rowid
        
        self.audioPlayer = QMediaPlayer()
        self.audioPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)
        
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Description", "", "", ""])
        self.setRowCount(1)
        
        #self.updateAudioListWidget()
        
    def getAudioFromDB(self, rowid):
        self.audioItemsDict = self.dbAdapter.audioFilenamesForDeckRowID(rowid)
        self.setRowCount(len(self.audioItemsDict))
        
        for i, row in enumerate(self.audioItemsDict):
            self.setItem(i, 0, QTableWidgetItem(row["description"]))
        
        self.updateAudioListWidget()
        
    def appendNewAudio(self):
        self.audioItemsDict.append({"description": None, "filename": None})
        self.insertRow(self.rowCount())
        self.updateAudioListWidget()
        
    def updateAudioListWidget(self):
        for i, row in enumerate(range(self.rowCount())):
            
            button_delete = QPushButton("delete", self)
            self.setCellWidget(row, DELETE_BUTTON_COLUMN, button_delete)
            button_delete.clicked.connect(partial(self.deleteAudioButtonClicked, row))
            
            if self.audioItemsDict[i]["filename"]:
                if self.status == self.STOPPED:
                    self.insertPlayButton(row)
                else:
                    if i == self.row:
                        self.insertStopPlayButton(row)
                    else:
                        self.insertPlayButton(row)
            else:
                if self.status == self.STOPPED:
                    self.insertRecordButton(row)
                else:
                    if i == self.row:
                        self.insertStopRecordButton(row)
                    else:
                        self.insertRecordButton(row)
            
            self.resizeColumnsToContents()
            
    def insertPlayButton(self, row):
        button_play = QPushButton("play", self)
        self.setCellWidget(row, PLAY_BUTTON_COLUMN, button_play)
        button_play.clicked.connect(partial(self.playButtonClicked, row))
        
    def insertStopPlayButton(self, row):
        button_stop = QPushButton("stop", self)
        self.setCellWidget(row, PLAY_BUTTON_COLUMN, button_stop)
        button_stop.clicked.connect(partial(self.stopPlayButtonClicked, row))
        
    def insertRecordButton(self, row):
        button_record = QPushButton("record", self)
        self.setCellWidget(row, RECORD_BUTTON_COLUMN, button_record)
        button_record.clicked.connect(partial(self.recordButtonClicked, row))
        
    def insertStopRecordButton(self, row):
        button_stop = QPushButton("stop", self)
        self.setCellWidget(row, RECORD_BUTTON_COLUMN, button_stop)
        button_stop.clicked.connect(partial(self.stopRecordButtonClicked, row))
            
    def deleteAudioButtonClicked(self, row):
        reply = QMessageBox.question(self, 'Delete Audio', "really?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.removeRow(row)
            self.updateAudioListWidget()
        
    def recordStopButtonClicked(self, row):
        #self.audioPlayer.play("./soldiers_joy.ogg")
        
        #self.audioRecorder = QDeckAudioItemWidget()
        #self.audioRecorder.initAudioInput()
        #self.audioRecorder.start()
        
        
        self.audioRecorder = RecordAudio()
        #self.audioRecorder.record("blaahh.ogg")
        
        #try:
            #self.audioRecordingDict[row]
        #except KeyError:
            
            #self.audioRecordingDict[row] = AudioRecording()
            #self.audioRecordingDict[row].setFilename("audioout.wav")
            
        #else:
            #if self.audioRecordingDict[row].recording:
                #self.stopButtonClicked(row)
            #else:
                #self.recordButtonClicked(row)
                
    def recordButtonClicked(self, row):
        self.stopPlayButtonClicked(row)
        self.stopRecordButtonClicked(row)
        print("recording")
        
        self.status = self.RECORDING
        self.row = row
        self.updateAudioListWidget()
        
    def stopRecordButtonClicked(self, row):
        print("stopping")
        
        self.status = self.STOPPED
        self.updateAudioListWidget()
            
    def playButtonClicked(self, row):
        filename = self.audioItemsDict[row]["filename"]
        filepath = path.join(self.deckpath, filename)
        url = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(filepath).absoluteFilePath())
        content = QMediaContent(url)
        self.audioPlayer.setMedia(content)
        self.audioPlayer.play()
        
        self.status = self.PLAYING
        self.row = row
        self.updateAudioListWidget()
        
    def stopPlayButtonClicked(self, row):
        self.audioPlayer.stop()
        
        self.status = self.STOPPED
        self.updateAudioListWidget()
        
    def mediaStatusChanged(self):
        #status = self.audioPlayer.mediaStatus()
        
        if self.audioPlayer.state() == QMediaPlayer.StoppedState:
            self.status = self.STOPPED
            self.updateAudioListWidget()
