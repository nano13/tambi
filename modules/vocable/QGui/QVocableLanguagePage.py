
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import Qt

from functools import partial
import os
from modules.vocable.vocableDbAdapter import VocableDbAdapter

class QVocableLanguagePage(QWidget):
    
    grid = None
    
    languageSelected = pyqtSignal(str, name='languageSelected')
    deckLearn = pyqtSignal(str, name='deckLearn')
    
    dbAdapter = VocableDbAdapter()
    defaultDeckPath = None
    
    listWidget = None
    tableWidget = None
    
    def __init__(self):
        super().__init__()
        
        self.tableWidget = QTableWidget()
    
    def setDefaultDeckPath(self, deckpath):
        self.defaultDeckPath = deckpath
    
    def vocableLanguagePage(self):
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        layout = self.setLayout(self.grid)
        
        self.tableWidget = self.createLanguageSelectList()
        self.grid.addWidget(self.tableWidget, 0, 0)
        
        return self
    
    def rescanLanguageList(self):
        print("rescanning")
        self.tableWidget = self.createLanguageSelectList()
        
    def createLanguageSelectList(self):
        language_list = self.getLanguages()
        
        self.tableWidget.setRowCount(len(language_list))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        
        for i, label in enumerate(language_list):
            item = QTableWidgetItem(label["name"])
            self.tableWidget.setItem(i, 0, item)
            # for read only:
            item.setFlags(Qt.ItemIsEnabled)
            
            if label["type"] == "simple":
                button_learn = QPushButton("learn", self)
                button_stats = QPushButton("stats", self)
                
                self.tableWidget.setCellWidget(i, 1, button_learn)
                self.tableWidget.setCellWidget(i, 2, button_stats)
                
                button_learn.clicked.connect(partial(self.tableButtonLearnClicked, label["name"]))
                button_stats.clicked.connect(partial(self.tableButtonStatsClicked, label["name"]))
        
        self.tableWidget.resizeColumnsToContents()
        
        return self.tableWidget
    
    def tableButtonLearnClicked(self, language):
        self.languageSelected.emit(language)
    
    def tableButtonStatsClicked(self, language):
        stats = self.dbAdapter.getStats(language)
        
        stats_tableWidget = QTableWidget()
        stats_tableWidget.setRowCount(len(stats))
        stats_tableWidget.setColumnCount(len(stats[0]))
        stats_tableWidget.setHorizontalHeaderLabels(["display", "gloss", "COUNT(word)", "known"])
        
        for i, line in enumerate(stats):
            for j, column in enumerate(line):
                item = QTableWidgetItem(str(stats[i][j]))
                stats_tableWidget.setItem(i, j, item)
                item.setFlags(Qt.ItemIsEnabled)
        
        stats_tableWidget.resizeColumnsToContents()
        self.grid.addWidget(stats_tableWidget, 2, 0)
    
    def itemClicked(self):
        language = self.listWidget.currentItem().text()
        self.languageSelected.emit(language)
    
    def getLanguages(self):
        languages = self.dbAdapter.getAvailableLanguages()
        
        languages_dict = []
        for lang in languages:
            languages_dict.append({"name": lang, "type": "simple"})
        
        return languages_dict
