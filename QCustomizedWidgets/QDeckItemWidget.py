
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from QCustomizedWidgets.QFreehandDrawWidget import QFreehandDrawView
from QCustomizedWidgets.QDeckAudioListWidget import QDeckAudioListWidget
from QCustomizedWidgets.QVkbdLineEdit import QVkbdLineEdit

from functools import partial
from os import path
import time, random, string

class QDeckItemWidget(QWidget):
    
    selectItem = pyqtSignal()
    deckpath = None
    dbAdapter = None
    current_rowid = None
    svg_filename = None
    
    def __init__(self):
        super().__init__()
        
    def setDeckpath(self, deckpath):
        self.deckpath = deckpath
        
    def setDbAdapter(self, dbAdapter):
        self.dbAdapter = dbAdapter
        
    def initializeAsEmpty(self):
        self.current_rowid = None
        self.svg_filename = None
        
        self.clearDrawView()
        self.nameLine.setText("")
        self.wordLine.setText("")
        self.translationLine.setText("")
        
        self.audioListWidget.initAudioListWidget(self.dbAdapter, self.deckpath, self.current_rowid)
        
    def initializeWithRowID(self, rowid):
        self.current_rowid = rowid
        
        self.clearDrawView()
        
        result = self.dbAdapter.selectDeckItem(rowid)
        
        svgsavepath = path.join(self.deckpath, result["svg_filename"])
        self.svg_filename = result["svg_filename"]
        self.freehandDrawWidget.loadView(svgsavepath)
        self.nameLine.setText(result["name"])
        self.wordLine.setText(result["word"])
        self.translationLine.setText(result["translation"])
        
        self.audioListWidget.initAudioListWidget(self.dbAdapter, self.deckpath, self.current_rowid)
        self.audioListWidget.getAudioFromDB(self.current_rowid)
        
    def newDeckPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        language_select_button = QPushButton("<<<")
        language_select_button.clicked.connect(self.languageSelectButtonClicked)
        
        clear_draw_view_button = QPushButton("clear draw area")
        clear_draw_view_button.clicked.connect(self.clearDrawViewButtonClicked)
        
        self.freehandDrawWidget = QFreehandDrawView(self)
        nameLabel = QLabel("name:")
        self.nameLine = QVkbdLineEdit() #QLineEdit()
        wordLabel = QLabel("word:")
        self.wordLine = QVkbdLineEdit() #QLineEdit()
        translationLabel = QLabel("translation:")
        self.translationLine = QVkbdLineEdit() #QLineEdit()
        self.audioListWidget = QDeckAudioListWidget()
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
        
        grid.setContentsMargins(0, 0, 0, 0)
        
        return self
    
    def languageSelectButtonClicked(self):
        self.audioListWidget.stopAllAudio()
        self.selectItem.emit()
        
    def newAudioButtonClicked(self):
        if self.current_rowid == None:
            reply = QMessageBox.question(self, 'Save first', 'please save the item first. Save now?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.saveButtonClicked()
                self.audioListWidget.setRowID(self.current_rowid)
                self.audioListWidget.appendNewAudio()
        else:
            self.audioListWidget.appendNewAudio()
    
    def saveButtonClicked(self):
        
        name = self.nameLine.text()
        word = self.wordLine.text()
        translation = self.translationLine.text()
        audio_filenames = None
        
        if self.current_rowid == None:
            svg_filename = str(int(time.time())) + self.randomword(5) + ".svg"
            
            self.freehandDrawWidget.saveView(path.join(self.deckpath, svg_filename))
            
            self.dbAdapter.saveDeckItem(name, word, translation, svg_filename)
            
            self.current_rowid = self.dbAdapter.getDeckItemRowID(name, word, translation, svg_filename)
            self.svg_filename = svg_filename
            
            self.audioListWidget.setRowID(self.current_rowid)
            
        else:
            self.freehandDrawWidget.saveView(path.join(self.deckpath, self.svg_filename))
            
            self.dbAdapter.updateDeckItem(self.current_rowid, name, word, translation, self.svg_filename)
            
        #self.audioListWidget.saveStateToDB(self.current_rowid)
        
        QMessageBox.information(self, "saved", "saved")
        
        # return to parent view:
        #self.selectItem.emit()
    
    def clearDrawViewButtonClicked(self):#
        reply = QMessageBox.question(self, 'Drop Drawing', "really?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clearDrawView()
            
    def clearDrawView(self):
        self.freehandDrawWidget.clearView()
        
    def randomword(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    
