
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import Qt

from functools import partial
from modules.vocable.vocableDbAdapter import VocableDbAdapter

class QVocableLanguagePage(QWidget):
    
    grid = None
    
    languageSelected = pyqtSignal(str, name='languageSelected')
    
    dbAdapter = VocableDbAdapter()
    
    listWidget = None
    tableWidget = None
    
    def __init__(self):
        super().__init__()
        
        
    def vocableLanguagePageOld(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        label_list = self.getLanguages()
        button_list = []
        for i, label in enumerate(label_list):
            button = QPushButton(label, self)
            button_list.append(button)
            
            grid.addWidget(button_list[i], i, 0)
            button_list[i].clicked.connect(partial(self.buttonClicked, label))
        
        return self
    
    def vocableLanguagePageList(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        language_list = self.getLanguages()
        
        self.listWidget = QListWidget()
        
        for i, label in enumerate(language_list):
            item = QListWidgetItem(label)
            self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.itemClicked)
            
        grid.addWidget(self.listWidget, 0, 0)
        
        return self
    
    def vocableLanguagePage(self):
        self.grid = QGridLayout()
        layout = self.setLayout(self.grid)
        
        language_list = self.getLanguages()
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(language_list))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        
        for i, label in enumerate(language_list):
            item = QTableWidgetItem(label)
            self.tableWidget.setItem(i, 0, item)
            # for read only:
            item.setFlags(Qt.ItemIsEnabled)
            
            button_learn = QPushButton("learn", self)
            button_stats = QPushButton("stats", self)
            
            self.tableWidget.setCellWidget(i, 1, button_learn)
            self.tableWidget.setCellWidget(i, 2, button_stats)
            
            button_learn.clicked.connect(partial(self.tableButtonLearnClicked, label))
            button_stats.clicked.connect(partial(self.tableButtonStatsClicked, label))
            
        self.tableWidget.resizeColumnsToContents()
        self.grid.addWidget(self.tableWidget, 0, 0)
        
        return self
    
    def buttonClicked(self, label):
        self.languageSelected.emit(label)
        
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
        self.grid.addWidget(stats_tableWidget, 1, 0)
        
    def itemClicked(self):
        language = self.listWidget.currentItem().text()
        self.languageSelected.emit(language)
        
    def getLanguages(self):
        languages = self.dbAdapter.getAvailableLanguages()
        
        return languages
