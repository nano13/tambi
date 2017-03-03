
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5 import QtSvg
from misc.deckDbAdapter import DeckDbAdapter

from os import path

class QDeckLearnWidget(QWidget):
    
    deckpath = None
    
    selectDeck = pyqtSignal()
    
    dataset = None
    number_of_data = None
    current_index = 0
    
    def __init__(self):
        super().__init__()
        
    def initialize(self, deckpath):
        self.deckpath = deckpath
        
        db_path = path.join(deckpath, "database.sqlite")
        self.dbAdapter = DeckDbAdapter()
        self.dbAdapter.initialize(db_path)
        
        deck_select_button = QPushButton("select deck")
        self.data_counter = QLabel()
        self.data_counter.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        deck_select_button.clicked.connect(self.selectDeckButtonClicked)
        
        
        self.current_name = QLabel()
        self.current_name.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.current_word = QLabel()
        self.current_word.setFont(QFont("Helvetica", 20))
        self.current_word.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.current_translation = QLabel()
        self.current_translation.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        button_prev = QPushButton('prev')
        button_next = QPushButton('next')
        button_show_translation = QPushButton('show translation')
        button_new_set = QPushButton('new set')
        button_known = QPushButton('known')
        button_not_known = QPushButton('not known')
        
        button_prev.clicked.connect(self.buttonPrevClicked)
        button_next.clicked.connect(self.buttonNextClicked)
        button_show_translation.clicked.connect(self.buttonShowTranslationClicked)
        button_new_set.clicked.connect(self.buttonNewSetClicked)
        button_known.clicked.connect(self.buttonKnownClicked)
        button_not_known.clicked.connect(self.buttonNotKnownClicked)
        
        self.dataset = self.dbAdapter.getDataset()
        
        self.number_of_data = len(self.dataset)
        self.data_counter.setText(str(self.current_index+1) + "/" + str(self.number_of_data))
        self.current_name.setText("")#self.dataset[self.current_index]['name'])
        try:
            self.current_word.setText(self.dataset[self.current_index]['word'])
        except IndexError:
            self.current_word.setText("ERROR: empty set")
        self.current_translation.setText("")#self.dataset[self.current_index]['translation'])
        
        try:
            self.svgWidget = QtSvg.QSvgWidget(path.join(self.deckpath, self.dataset[self.current_index]['svg_filename']))
        except IndexError:
            self.svgWidget = QtSvg.QSvgWidget()
        
        self.svgWidget.setFixedSize(300, 150)
        self.svgWidget.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        
        if not self.layout():
            self.grid = QGridLayout()
            self.grid.setContentsMargins(0, 0, 0, 0)
            self.grid.addWidget(deck_select_button, 0, 0)
            self.grid.addWidget(self.data_counter, 0, 2)
            self.grid.addWidget(self.svgWidget, 1, 1)
            
            self.grid.addWidget(self.current_name, 4, 1)
            self.grid.addWidget(self.current_word, 5, 1)
            self.grid.addWidget(self.current_translation, 6, 1)
            
            self.grid.addWidget(button_prev, 7, 0)
            self.grid.addWidget(button_next, 8, 0)
            self.grid.addWidget(button_show_translation, 7, 1)
            self.grid.addWidget(button_new_set, 8, 1)
            self.grid.addWidget(button_known, 7, 2)
            self.grid.addWidget(button_not_known, 8, 2)
            
            layout = self.setLayout(self.grid)
        
    
    def selectDeckButtonClicked(self):
        self.selectDeck.emit()
        
    def buttonPrevClicked(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.dataset)-1
        
        self.setTexts()
        
    def buttonNextClicked(self):
        if self.current_index < len(self.dataset)-1:
            self.current_index += 1
        else:
            self.current_index = 0
        
        self.setTexts()
        
    def setTexts(self):
        try:
            self.current_word.setText(self.dataset[self.current_index]['word'])
        except IndexError:
            self.current_word.setText('ERROR: empty set')
        
        
        self.current_name.setText("")
        self.current_translation.setText("")
        
        self.svgWidget.load(path.join(self.deckpath, self.dataset[self.current_index]['svg_filename']))
        
        self.data_counter.setText(str(self.current_index+1) + "/" + str(self.number_of_data))
        
    def buttonShowTranslationClicked(self):
        try:
            self.current_name.setText(self.dataset[self.current_index]['name'])
            self.current_translation.setText(self.dataset[self.current_index]['translation'])
        except IndexError:
            self.current_name.setText('ERROR: empty set')
            self.current_translation.setText('ERROR: empty set')
        
    def buttonNewSetClicked(self):
        print("new set")
    def buttonKnownClicked(self):
        print("known")
    def buttonNotKnownClicked(self):
        print("not known")
