
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTableWidget, QTableWidgetItem

from misc.audioRecording import RecordAudio
from QCustomizedWidgets.QDeckAudioItemWidget import QDeckAudioItemWidget
from misc.playAudio import PlayAudio

from functools import partial

class QNewDeckAudioListWidget(QTableWidget):
    
    deckpath = None
    current_deck_rowid = None
    dbAdapter = None
    
    audioFilesDict = {}
    audioPlayer = PlayAudio()
    
    def __init__(self):
        super().__init__()
        
    def initAudioListWidget(self, dbAdapter, deckpath, current_rowid):
        self.dbAdapter = dbAdapter
        self.deckpath = deckpath
        self.current_deck_rowid = current_rowid
        
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Description", "", "", ""])
        self.setRowCount(1)
        
        self.updateAudioListWidget()
        
    def updateAudioListWidget(self):
        for row in range(self.rowCount()):
            button_delete = QPushButton("delete", self)
            self.setCellWidget(row, 3, button_delete)
            button_delete.clicked.connect(partial(self.deleteAudioButtonClicked, row))
            
            button_record = QPushButton("record", self)
            self.setCellWidget(row, 1, button_record)
            button_record.clicked.connect(partial(self.recordStopButtonClicked, row))
            
            button_play = QPushButton("play", self)
            self.setCellWidget(row, 2, button_play)
            button_play.clicked.connect(partial(self.playButtonClicked, row))
            
            self.resizeColumnsToContents()
            
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
        print("recording")
        self.audioRecordingDict[row].startRecording()
        
    def stopButtonClicked(self, row):
        print("stopping")
        self.audioRecording.stopRecording()
            
    def playButtonClicked(self, row):
        self.audioRecorder.stop()
