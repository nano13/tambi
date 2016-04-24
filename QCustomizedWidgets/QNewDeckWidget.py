
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSignal

from QCustomizedWidgets.QFreehandDrawWidget import QFreehandDrawWidget

from functools import partial

class QNewDeckWidget(QWidget):
    
    selectLanguage = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def newDeckPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        language_select_button = QPushButton("select deck")
        language_select_button.clicked.connect(self.languageSelectButtonClicked)
        
        self.freehandDrawWidget = QFreehandDrawWidget()
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
        grid.addWidget(self.freehandDrawWidget, 1, 0, 1, 3)
        grid.addWidget(wordLabel, 2, 0)
        grid.addWidget(self.wordLine, 2, 1, 1, 2)
        grid.addWidget(translationLabel, 4, 0)
        grid.addWidget(self.translationLine, 4, 1, 1, 2)
        grid.addWidget(self.audioListWidget, 6, 0, 2, 3)
        grid.addWidget(newAudioButton, 9, 0)
        grid.addWidget(saveButton, 9, 2)
        
        return self
    
    def languageSelectButtonClicked(self):
        self.selectLanguage.emit()
        
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
        pass
