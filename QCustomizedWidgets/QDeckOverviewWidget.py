
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtSvg
#from QCustomizedWidgets.QNewDeckWidget import QNewDeckWidget
from misc.deckDbAdapter import DeckDbAdapter

from os import path, remove
from functools import partial

class QDeckOverviewWidget(QWidget):
    
    deckpath = None
    
    selectDeck = pyqtSignal()
    createNewItem = pyqtSignal(str, object)
    editDeckItem = pyqtSignal(str, object, int)
    
    tableWidget = None
    
    def __init__(self):
        super().__init__()
        
    def update(self):
        self.initWithDbData()
        
    def initializeDeckOverview(self, deckpath):
        self.deckpath = deckpath
        
        db_path = path.join(deckpath, "database.sqlite")
        #self.dbAdapter = DeckDbAdapter(path.join(deckpath, "database.sqlite"))
        self.dbAdapter = DeckDbAdapter()
        self.dbAdapter.initDB(db_path)
        
        deck_select_button = QPushButton("select deck")
        deck_select_button.clicked.connect(self.selectDeckButtonClicked)
        
        new_item_button = QPushButton("new item")
        new_item_button.clicked.connect(self.newItemButtonClicked)
        #self.tableWidget.setCellWidget(0, 0, new_item_button)
        
        self.initTableWidget()
        
        if not self.layout():
            self.grid = QGridLayout()
            self.grid.setContentsMargins(0, 0, 0, 0)
            self.grid.addWidget(deck_select_button, 0, 0)
            self.grid.addWidget(self.tableWidget, 1, 0, 1, 3)
            self.grid.addWidget(new_item_button, 2, 0)
            
            layout = self.setLayout(self.grid)
        
        self.initWithDbData()
        
    def initTableWidget(self):
        if not self.tableWidget:
            self.tableWidget = QTableWidget()
            
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["", "", "id", "name", "word", "translation", "svg", "audio"])
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        
        
    def initWithDbData(self):
        self.tableWidget.clear()
        
        data = self.dbAdapter.selectDeckItems()
        self.tableWidget.setRowCount(len(data))
        
        for i, line in enumerate(data):
            rowid = line["rowid"]
            name = line["name"]
            word = line["word"]
            translation = line["translation"]
            svg_filename = line["svg_filename"]
            audio_filenames = line["audio_filenames"]
            
            svgWidget = QtSvg.QSvgWidget(path.join(self.deckpath, svg_filename))
            #svgWidget.setGeometry(50,50,759,668)
            svgWidget.setFixedSize(60, 30)
            
            edit_button = QPushButton("edit")
            edit_button.clicked.connect(partial(self.editRowButtonClicked, rowid))
            delete_button = QPushButton("delete")
            delete_button.clicked.connect(partial(self.deleteRowButtonClicked, rowid))
            
            self.tableWidget.setCellWidget(i, 0, edit_button)
            self.tableWidget.setCellWidget(i, 1, delete_button)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(rowid)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(word))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(translation))
            self.tableWidget.setCellWidget(i, 6, svgWidget)
            
        self.tableWidget.resizeColumnsToContents()
            
    def selectDeckButtonClicked(self):
        self.selectDeck.emit()
        
    def newItemButtonClicked(self):
        self.createNewItem.emit(self.deckpath, self.dbAdapter)
        
    def editRowButtonClicked(self, rowid):
        self.editDeckItem.emit(self.deckpath, self.dbAdapter, int(rowid))
    
    def deleteRowButtonClicked(self, rowid):
        
        delete_msg = "really?"
        reply = QMessageBox.question(self, 'Delete', delete_msg, QMessageBox.Yes, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            svg_filename, audio_filenames = self.dbAdapter.deleteItem(rowid)
            if svg_filename:
                remove(path.join(self.deckpath, svg_filename))
                pass
            
            for audio in audio_filenames:
                remove(path.join(self.deckpath, audio))
            
            self.initWithDbData()
