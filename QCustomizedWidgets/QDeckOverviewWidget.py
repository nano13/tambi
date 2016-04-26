

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal
#from QCustomizedWidgets.QNewDeckWidget import QNewDeckWidget
from misc.deckDbAdapter import DeckDbAdapter

from os import path
from functools import partial

class QDeckOverviewWidget(QWidget):
    
    deckpath = None
    
    selectDeck = pyqtSignal()
    createNewItem = pyqtSignal(str, object)
    
    def __init__(self):
        super().__init__()
        
    def update(self):
        self.initWithDbData()
        
    def initializeDeckOverview(self, deckpath):
        self.deckpath = deckpath
        
        self.dbAdapter = DeckDbAdapter(path.join(deckpath, "database.sqlite"))
        
        deck_select_button = QPushButton("select deck")
        deck_select_button.clicked.connect(self.selectDeckButtonClicked)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["", "id", "name", "word", "translation", "svg", "#audio"])
        self.tableWidget.verticalHeader().hide()
        
        new_item_button = QPushButton("new item")
        new_item_button.clicked.connect(self.newItemButtonClicked)
        #self.tableWidget.setCellWidget(0, 0, new_item_button)
        
        self.grid = QGridLayout()
        self.grid.addWidget(deck_select_button, 0, 0)
        self.grid.addWidget(self.tableWidget, 1, 0, 1, 3)
        self.grid.addWidget(new_item_button, 2, 0)
        
        layout = self.setLayout(self.grid)
        
        self.initWithDbData()
        
    def initWithDbData(self):
        data = self.dbAdapter.selectDeckItems()
        self.tableWidget.setRowCount(len(data))
        
        for i, line in enumerate(data):
            rowid = line["rowid"]
            name = line["name"]
            word = line["word"]
            translation = line["translation"]
            svg_filename = line["svg_filename"]
            audio_filenames = line["audio_filenames"]
            
            edit_button = QPushButton("edit")
            edit_button.clicked.connect(partial(self.editRowButtonClicked, rowid))
            delete_button = QPushButton("delete")
            delete_button.clicked.connect(partial(self.deleteRowButtonClicked, rowid))
            
            self.tableWidget.setCellWidget(i, 0, edit_button)
            self.tableWidget.setCellWidget(i, 1, delete_button)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(rowid))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(word))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(translation))
            
        self.tableWidget.resizeColumnsToContents()
            
    def selectDeckButtonClicked(self):
        self.selectDeck.emit()
        
    def newItemButtonClicked(self):
        self.createNewItem.emit(self.deckpath, self.dbAdapter)
        
    def editRowButtonClicked(self, rowid):
        print(rowid)
    
    def deleteRowButtonClicked(self, rowid):
        #TODO: Delete Files!
        self.dbAdapter.deleteItem(rowid)
        self.initWithDbData()