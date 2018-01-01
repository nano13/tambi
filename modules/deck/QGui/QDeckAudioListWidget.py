
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioRecorder, QAudioEncoderSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QFileInfo, QProcess

#from QCustomizedWidgets.QVoiceRecorder import QVoiceRecorder
from configs.configFiles import ConfigFile

from functools import partial
from os import path, remove
import os, shutil
import time, random, string, platform

PLAY_BUTTON_COLUMN = 1
RECORD_BUTTON_COLUMN = 1
DELETE_BUTTON_COLUMN = 2
OPEN_FILE_BUTTON_COLUMN = 3
EDIT_FILE_BUTTON = 4
FILE_NAME_COLUMN = 5

class QDeckAudioListWidget(QTableWidget):
    
    deckpath = None
    current_deck_rowid = None
    dbAdapter = None
    
    current_rowid = None
    
    config = ConfigFile(None, None)
    
    audioItemsDict = []
    audioPlayer = None
    audioRecorder = None
    
    STOPPED = 0
    RECORDING = 1
    PLAYING = 2
    status = 0
    row = None
    
    default_import_path = os.path.expanduser('~')
    
    def __init__(self):
        super().__init__()
        
    def setRowID(self, rowid):
        self.current_rowid = rowid
        
    def initAudioListWidget(self, dbAdapter, deckpath, current_rowid):
        self.audioItemsDict = []
        
        self.dbAdapter = dbAdapter
        self.deckpath = deckpath
        self.current_rowid = current_rowid
        
        self.audioPlayer = QMediaPlayer()
        self.audioPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)
        
        os_name = platform.uname()[0]
        if os_name == "Windows" or os_name == "Darwin":
            self.audioRecorder = QAudioRecorder()
        else:
            from modules.deck.gstAudioRecorder import GstAudioRecorder
            self.audioRecorder = GstAudioRecorder()
        
        settings = QAudioEncoderSettings()
        
        audioformat = self.config.readVar('vocable', 'audioformat')
        if audioformat == 'ogg':
            settings.setCodec("audio/vorbis")
            self.audioRecorder.setContainerFormat("ogg")
        elif audioformat == 'mp3':
            settings.setCodec("audio/mpeg")
            self.audioRecorder.setContainerFormat("mp3")
        elif audioformat == 'amr':
            settings.setCodec("audio/amr")
        else:
            settings.setCodec("audio/PCM")
            self.audioRecorder.setContainerFormat("wav")
        
        self.audioRecorder.setEncodingSettings(settings)
        
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["description", "", "", "", "", "filename"])
        self.setRowCount(0)
        
        self.itemChanged.connect(self.onItemChanged)
        
    def getAudioFromDB(self, rowid):
        self.audioItemsDict = self.dbAdapter.audioFilenamesForDeckRowID(rowid)
        self.setRowCount(len(self.audioItemsDict))
        
        for i, row in enumerate(self.audioItemsDict):
            self.setItem(i, 0, QTableWidgetItem(row["description"]))
        
        self.updateAudioListWidget()
        
    def appendNewAudio(self):
        self.audioItemsDict.append({"rowid": None, "description": "", "filename": None})
        self.insertRow(self.rowCount())
        self.updateAudioListWidget()
        
    def updateAudioListWidget(self):
        for i, row in enumerate(range(self.rowCount())):
            
            button_delete = QPushButton()
            button_delete.setIcon(QIcon.fromTheme('edit-delete'))
            self.setCellWidget(row, DELETE_BUTTON_COLUMN, button_delete)
            button_delete.clicked.connect(partial(self.deleteAudioButtonClicked, row))
            
            button_open_file = QPushButton()
            button_open_file.setIcon(QIcon.fromTheme('document-open'))
            self.setCellWidget(row, OPEN_FILE_BUTTON_COLUMN, button_open_file)
            button_open_file.clicked.connect(partial(self.importAudioFileClicked, row))
            
            button_edit_file = QPushButton()
            #button_edit_file.setIcon(QIcon.fromTheme('audio-x-generic'))
            button_edit_file.setIcon(QIcon('./assets/icons/audacity.jpg'))
            self.setCellWidget(row, EDIT_FILE_BUTTON, button_edit_file)
            button_edit_file.clicked.connect(partial(self.editAudioFileClicked, row))
            
            self.setItem(row, FILE_NAME_COLUMN, QTableWidgetItem(str(self.audioItemsDict[row]["filename"])))
            
            if self.status == self.STOPPED:
                if self.audioItemsDict[i]["filename"]:
                    self.insertPlayButton(row)
                else:
                    self.insertRecordButton(row)
            
            elif self.status == self.PLAYING:
                if i == self.row:
                    self.insertStopPlayButton(row)
                else:
                    if not self.audioItemsDict[i]["filename"]:
                        self.insertRecordButton(row)
                    else:
                        self.insertPlayButton(row)
            
            elif self.status == self.RECORDING:
                if i == self.row:
                    self.insertStopRecordButton(row)
                else:
                    if self.audioItemsDict[i]["filename"]:
                        self.insertPlayButton(row)
                    else:
                        self.insertRecordButton(row)
            
            self.resizeColumnsToContents()
            
    def insertPlayButton(self, row):
        button_play = QPushButton()
        button_play.setIcon(QIcon.fromTheme('media-playback-start'))
        self.setCellWidget(row, PLAY_BUTTON_COLUMN, button_play)
        button_play.clicked.connect(partial(self.playButtonClicked, row))
        
    def insertStopPlayButton(self, row):
        button_stop = QPushButton()
        button_stop.setIcon(QIcon.fromTheme('media-playback-stop'))
        self.setCellWidget(row, PLAY_BUTTON_COLUMN, button_stop)
        button_stop.clicked.connect(partial(self.stopPlayButtonClicked, row))
        
    def insertRecordButton(self, row):
        button_record = QPushButton()
        button_record.setIcon(QIcon.fromTheme('media-record'))
        self.setCellWidget(row, RECORD_BUTTON_COLUMN, button_record)
        button_record.clicked.connect(partial(self.recordButtonClicked, row))
        
    def insertStopRecordButton(self, row):
        button_stop = QPushButton()
        button_stop.setIcon(QIcon.fromTheme('media-playback-stop'))
        self.setCellWidget(row, RECORD_BUTTON_COLUMN, button_stop)
        button_stop.clicked.connect(partial(self.stopRecordButtonClicked, row))
            
    def deleteAudioButtonClicked(self, row):
        reply = QMessageBox.question(self, 'Delete Audio', "really?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.removeRow(row)
            
            rowid = self.audioItemsDict[row]["rowid"]
            if rowid:
                self.dbAdapter.deleteAudioItem(rowid)
                
            filename = self.audioItemsDict[row]["filename"]
            if filename:
                self.dbAdapter.deleteAudioItemByFilename(filename)
                filepath = path.join(self.deckpath, filename)
                if path.exists(filepath):
                    remove(filepath)
            
            del self.audioItemsDict[row]
            self.updateAudioListWidget()
    
    def importAudioFileClicked(self, row):
        file_path = QFileDialog.getOpenFileName(self, 'Please select an Audio File', self.default_import_path)
        self.default_import_path = file_path[0]
        filename = file_path[0].split(os.sep)[::-1][0]
        target_path = os.path.join(self.deckpath, filename)
        #if not os.path.exists(target_path):
        try:
            shutil.copyfile(file_path[0], target_path)
        except FileNotFoundError:
            """ there is simply no file to copy """
            pass
        else:
            self.audioItemsDict[row]["filename"] = filename
            self.status = self.STOPPED
            self.updateAudioListWidget()
            
            self.saveStateToDB(self.current_rowid)
    
    def editAudioFileClicked(self, row):
        filename = self.audioItemsDict[row]["filename"]
        target_path = os.path.join(self.deckpath, filename)
        
        self.process = QProcess()
        self.process.start("audacity "+target_path)
    
    def recordButtonClicked(self, row):
        self.stopPlayButtonClicked(row)
        self.stopRecordButtonClicked(row)
        
        extension = '.wav'
        audioformat = self.config.readVar('vocable', 'audioformat')
        if audioformat == 'ogg':
            extension = '.ogg'
        elif audioformat == 'mp3':
            extension = '.mp3'
        elif audioformat == 'amr':
            extension = '.amr'
        filename = str(int(time.time())) + self.randomword(5) + extension
        filepath = os.path.join(self.deckpath, filename)
        print(filepath)
        
        url = QUrl.fromLocalFile(QFileInfo(filepath).absoluteFilePath())
        self.audioRecorder.setOutputLocation(url)
        self.audioRecorder.record()
        
        self.audioItemsDict[row]["filename"] = filename
        
        self.status = self.RECORDING
        self.row = row
        self.updateAudioListWidget()
        
        self.saveStateToDB(self.current_rowid)
        
    def stopRecordButtonClicked(self, row):
        self.stopPlayButtonClicked(row)
        self.audioRecorder.stop()
        
        self.status = self.STOPPED
        self.updateAudioListWidget()
            
    def playButtonClicked(self, row):
        self.stopRecordButtonClicked(row)
        
        filename = self.audioItemsDict[row]["filename"]
        filepath = path.join(self.deckpath, filename)
        url = QUrl.fromLocalFile(QFileInfo(filepath).absoluteFilePath())
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
        
    def stopAllAudio(self):
        row = 1
        self.stopPlayButtonClicked(row)
        self.stopRecordButtonClicked(row)
        self.status = self.STOPPED
        
    def mediaStatusChanged(self):
        status = self.audioPlayer.mediaStatus()
        
        if status == 7:
            self.stopAllAudio()
    
    def onItemChanged(self):
        
        for i in range(self.rowCount()):
            item = self.item(i, 0)
            if item:
                cell_text = self.item(i, 0).text()
                self.audioItemsDict[i]["description"] = cell_text
            
    def saveStateToDB(self, deck_rowid):
        self.dbAdapter.saveAudioDict(self.audioItemsDict, deck_rowid)
    
    def randomword(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
