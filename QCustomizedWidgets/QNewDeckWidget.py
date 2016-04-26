
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from QCustomizedWidgets.QFreehandDrawWidget import QFreehandDrawView
#from misc.deckDbAdapter import DeckDbAdapter

from functools import partial
from os import path
import time, random, string

class QNewDeckWidget(QWidget):
    
    selectItem = pyqtSignal()
    deckpath = None
    dbAdapter = None
    
    def __init__(self):
        super().__init__()
        
    def setDeckpath(self, deckpath):
        self.deckpath = deckpath
        
    def setDbAdapter(self, dbAdapter):
        self.dbAdapter = dbAdapter
        
    def newDeckPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        language_select_button = QPushButton("select item")
        language_select_button.clicked.connect(self.languageSelectButtonClicked)
        
        clear_draw_view_button = QPushButton("clear draw area")
        clear_draw_view_button.clicked.connect(self.clearDrawViewButtonClicked)
        
        #self.freehandDrawWidget = QFreehandDrawWidget()
        self.freehandDrawWidget = QFreehandDrawView(self)
        nameLabel = QLabel("name:")
        self.nameLine = QLineEdit()
        wordLabel = QLabel("word:")
        self.wordLine = QLineEdit()
        translationLabel = QLabel("translation:")
        self.translationLine = QLineEdit()
        self.audioListWidget = QTableWidget()
        self.initAudioListWidget()
        newAudioButton = QPushButton("new audio")
        newAudioButton.clicked.connect(self.newAudioButtonClicked)
        saveButton = QPushButton("save")
        saveButton.clicked.connect(self.saveButtonClicked)
        
        grid.addWidget(language_select_button, 0, 0)
        grid.addWidget(clear_draw_view_button, 0, 3)
        grid.addWidget(self.freehandDrawWidget, 1, 0, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(nameLabel, 2, 0)
        grid.addWidget(self.nameLine, 2, 1, 1, 3)
        grid.addWidget(wordLabel, 3, 0)
        grid.addWidget(self.wordLine, 3, 1, 1, 3)
        grid.addWidget(translationLabel, 4, 0)
        grid.addWidget(self.translationLine, 4, 1, 1, 3)
        grid.addWidget(self.audioListWidget, 5, 0, 1, 4)
        grid.addWidget(newAudioButton, 6, 0)
        grid.addWidget(saveButton, 6, 3)
        
        #self.freehandDrawWidget.loadView("outtest.svg")
        
        return self
    
    def languageSelectButtonClicked(self):
        self.selectItem.emit()
        
    def initAudioListWidget(self):
        self.audioListWidget.setColumnCount(4)
        self.audioListWidget.setHorizontalHeaderLabels(["Description", "", "", ""])
        self.audioListWidget.setRowCount(1)
        
        self.updateAudioListWidget()
        
        
    def updateAudioListWidget(self):
        for row in range(self.audioListWidget.rowCount()):
            button_delete = QPushButton("delete", self)
            self.audioListWidget.setCellWidget(row, 3, button_delete)
            button_delete.clicked.connect(partial(self.deleteAudioButtonClicked, row))
            
            button_record = QPushButton("record", self)
            self.audioListWidget.setCellWidget(row, 1, button_record)
            button_record.clicked.connect(partial(self.recordButtonClicked, row))
            
            button_play = QPushButton("play", self)
            self.audioListWidget.setCellWidget(row, 2, button_play)
            button_play.clicked.connect(partial(self.playButtonClicked, row))
            
            self.audioListWidget.resizeColumnsToContents()
        
    def newAudioButtonClicked(self):
        row_position = self.audioListWidget.rowCount()
        self.audioListWidget.insertRow(row_position)
        self.updateAudioListWidget()
        
    def deleteAudioButtonClicked(self, row):
        self.audioListWidget.removeRow(row)
        self.updateAudioListWidget()
        
    def recordButtonClicked(self, row):
        pass
    
    def playButtonClicked(self, row):
        pass
    
    def saveButtonClicked(self):
        svg_filename = str(int(time.time())) + self.randomword(5) + ".svg"
        
        self.freehandDrawWidget.saveView(path.join(self.deckpath, svg_filename))
        
        name = self.nameLine.text()
        word = self.wordLine.text()
        translation = self.translationLine.text()
        audio_filenames = None
        
        self.dbAdapter.saveDeckItem(name, word, translation, svg_filename, audio_filenames)
        
        
    
    def clearDrawViewButtonClicked(self):
        self.freehandDrawWidget.clearView()
        
    def randomword(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
