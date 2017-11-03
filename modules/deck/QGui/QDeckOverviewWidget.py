
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5 import QtSvg
from PyQt5.QtGui import QIcon, QPixmap

from QCustomizedWidgets.QAudioItems import QAudioItems

from modules.deck.deckDbAdapter import DeckDbAdapter
from misc.unicodeFonts import UnicodeFonts

from os import path, remove
from functools import partial

COLUMN_OFFSET = 9

class QDeckOverviewWidget(QWidget):
    
    deckpath = None
    
    selectDeck = pyqtSignal()
    createNewItem = pyqtSignal(str, object)
    editDeckItem = pyqtSignal(str, object, int)
    
    tableWidget = None
    audioWidget = None
    
    def __init__(self):
        super().__init__()
        
        self.unicodeFonts = UnicodeFonts()
        
    def initialize(self, deckpath):
        self.deckpath = deckpath
        
        db_path = path.join(deckpath, "database.sqlite")
        self.dbAdapter = DeckDbAdapter()
        self.dbAdapter.initialize(db_path)
        
        deck_select_button = QPushButton("<<<")
        deck_select_button.clicked.connect(self.selectDeckButtonClicked)
        
        new_item_button = QPushButton("new item")
        new_item_button.clicked.connect(self.newItemButtonClicked)
        
        stop_all_sounds_button = QPushButton("stop all sounds")
        stop_all_sounds_button.clicked.connect(self.stopAllSounds)
        
        self.initTableWidget()
        
        if not self.layout():
            self.grid = QGridLayout()
            self.grid.setContentsMargins(0, 0, 0, 0)
            self.grid.addWidget(deck_select_button, 0, 0)
            self.grid.addWidget(self.tableWidget, 1, 0, 1, 3)
            self.grid.addWidget(new_item_button, 2, 0)
            self.grid.addWidget(stop_all_sounds_button, 2, 2)
            
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
        #data = self.dbAdapter.selectDeckItemsWithAudio()
        self.tableWidget.setRowCount(len(data))
        
        max_audio_count = self.dbAdapter.getMaxAudioCount()
        self.audioWidget = QAudioItems(self.deckpath, self.tableWidget, max_audio_count, COLUMN_OFFSET)
        
        for i, line in enumerate(data):
            rowid = line["rowid"]
            order_index = line["order_index"]
            name = line["name"]
            word = line["word"]
            phonetical = line["phonetical"]
            translation = line["translation"]
            svg_filename = line["svg_filename"]
            image_filename = None
            imageWidget = QLabel()
            try:
                image_filename = line["image"]
            except:
                """ maybe we have an image, maybe not ... """
                pass
            else:
                pixmap = QPixmap()
                try:
                    pixmap.load(path.join(self.deckpath, image_filename))
                except TypeError:
                    """ probably we have an None-image here """
                    pass
                else:
                    pixmap = pixmap.scaled(QSize(60, 30), Qt.KeepAspectRatio)
                    imageWidget.setPixmap(pixmap)
            
            audio_filenames = self.dbAdapter.audioFilenamesForDeckRowID(rowid)
            
            try:
                svgWidget = QtSvg.QSvgWidget(path.join(self.deckpath, svg_filename))
            except TypeError:
                svgWidget = QtSvg.QSvgWidget()
            #svgWidget.setGeometry(50,50,759,668)
            svgWidget.setFixedSize(60, 30)
            
            edit_button = QPushButton()#"edit")
            edit_button.setIcon(QIcon.fromTheme("document-properties"))
            edit_button.clicked.connect(partial(self.editRowButtonClicked, rowid))
            delete_button = QPushButton()#"delete")
            delete_button.setIcon(QIcon.fromTheme('edit-delete'))
            delete_button.clicked.connect(partial(self.deleteRowButtonClicked, rowid))
            
            self.tableWidget.setCellWidget(i, 0, edit_button)
            self.tableWidget.setCellWidget(i, 1, delete_button)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(order_index)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(word))
            
            phonetical_item = QTableWidgetItem(phonetical)
            self.unicodeFonts.setFont('ipa', phonetical_item)
            self.tableWidget.setItem(i, 5, phonetical_item)
            
            self.tableWidget.setItem(i, 6, QTableWidgetItem(translation))
            self.tableWidget.setCellWidget(i, 7, svgWidget)
            self.tableWidget.setCellWidget(i, 8, imageWidget)
            
            #if audio_filenames:
            print("AUDIO_FILENAMES")
            print(audio_filenames)
            self.audioWidget.appendPlayButtonsDict(audio_filenames, i)
            
        #column_count = self.audioWidget.getMaxColCount()
        #self.tableWidget.setColumnCount(column_count)
        self.tableWidget.setColumnCount(COLUMN_OFFSET + max_audio_count)
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
                if path.exists(path.join(self.deckpath, audio)):
                    remove(path.join(self.deckpath, audio))
            
            self.initWithDbData()
    
    def stopAllSounds(self):
        self.audioWidget.stopAllSounds()
