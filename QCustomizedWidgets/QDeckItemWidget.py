
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QMessageBox, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap

from QCustomizedWidgets.QFreehandDrawWidget import QFreehandDrawView
from QCustomizedWidgets.QDeckAudioListWidget import QDeckAudioListWidget
from QCustomizedWidgets.QVkbdLineEdit import QVkbdLineEdit

from functools import partial
from os import path, sep, remove
import time, random, string, shutil

class QDeckItemWidget(QWidget):
    
    selectItem = pyqtSignal()
    deckpath = None
    dbAdapter = None
    current_rowid = None
    svg_filename = None
    
    dataset = None
    
    default_import_path = path.expanduser('~')
    
    def __init__(self):
        super().__init__()
        
        style = """
        QLineEdit{ font-size: 25px; }
        """
        import platform
        if not platform.system() == 'darwin':
            """ this does look uggly on mac """
            self.setStyleSheet(style)
        
    def setDeckpath(self, deckpath):
        self.deckpath = deckpath
        
    def setDbAdapter(self, dbAdapter):
        self.dbAdapter = dbAdapter
        
    def initializeAsEmpty(self):
        self.current_rowid = None
        self.svg_filename = None
        
        self.clearDrawView()
        self.imageView.clear()
        self.nameLine.setText("")
        self.wordLine.setText("")
        self.phoneticalLine.setText("")
        self.translationLine.setText("")
        
        self.audioListWidget.initAudioListWidget(self.dbAdapter, self.deckpath, self.current_rowid)
        
    def initializeWithRowID(self, rowid):
        self.current_rowid = rowid
        
        self.clearDrawView()
        pixmap = QPixmap()
        self.imageView.setPixmap(pixmap)
        
        result = self.dbAdapter.selectDeckItem(rowid)
        self.dataset = result
        
        svgsavepath = path.join(self.deckpath, result["svg_filename"])
        self.svg_filename = result["svg_filename"]
        self.freehandDrawWidget.loadView(svgsavepath)
        self.nameLine.setText(result["name"])
        self.wordLine.setText(result["word"])
        self.phoneticalLine.setText(result["phonetical"])
        self.translationLine.setText(result["translation"])
        
        if 'image' in result and result['image']:
            pixmap = QPixmap()
            pixmap.load(path.join(self.deckpath, result['image']))
            pixmap = pixmap.scaled(QSize(660, 440), Qt.KeepAspectRatio)
            self.imageView.setPixmap(pixmap)
            self.imageView.show()
        
        self.audioListWidget.initAudioListWidget(self.dbAdapter, self.deckpath, self.current_rowid)
        self.audioListWidget.getAudioFromDB(self.current_rowid)
        
    def newDeckPage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        language_select_button = QPushButton("<<<")
        language_select_button.clicked.connect(self.languageSelectButtonClicked)
        
        import_image_button = QPushButton("add image from file")
        import_image_button.setIcon(QIcon.fromTheme('document-open'))
        import_image_button.clicked.connect(self.importImage)
        
        delete_image_button = QPushButton("clear image")
        delete_image_button.setIcon(QIcon.fromTheme('edit-delete'))
        delete_image_button.clicked.connect(self.deleteImage)
        
        clear_draw_view_button = QPushButton("clear draw area")
        clear_draw_view_button.clicked.connect(self.clearDrawViewButtonClicked)
        
        self.freehandDrawWidget = QFreehandDrawView(self)
        self.freehandDrawWidget.hide()
        self.imageView = QLabel()
        #self.imageView.hide()
        nameLabel = QLabel("name:")
        self.nameLine = QVkbdLineEdit() #QLineEdit()
        wordLabel = QLabel("word:")
        self.wordLine = QVkbdLineEdit() #QLineEdit()
        translationLabel = QLabel("translation:")
        self.phoneticalLine = QVkbdLineEdit()
        phoneticalLabel = QLabel("phonetical:")
        self.translationLine = QVkbdLineEdit() #QLineEdit()
        self.audioListWidget = QDeckAudioListWidget()
        newAudioButton = QPushButton("new audio")
        newAudioButton.clicked.connect(self.newAudioButtonClicked)
        saveButton = QPushButton("save")
        saveButton.clicked.connect(self.saveButtonClicked)
        
        grid.addWidget(language_select_button, 0, 0)
        grid.addWidget(import_image_button, 0, 2)
        grid.addWidget(delete_image_button, 0, 3)
        #grid.addWidget(clear_draw_view_button, 0, 3)
        #grid.addWidget(self.freehandDrawWidget, 1, 0, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.imageView, 1, 0, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(nameLabel, 2, 0)
        grid.addWidget(self.nameLine, 2, 1, 1, 3)
        grid.addWidget(wordLabel, 3, 0)
        grid.addWidget(self.wordLine, 3, 1, 1, 3)
        grid.addWidget(phoneticalLabel, 4, 0)
        grid.addWidget(self.phoneticalLine, 4, 1, 1, 3)
        grid.addWidget(translationLabel, 5, 0)
        grid.addWidget(self.translationLine, 5, 1, 1, 3)
        grid.addWidget(self.audioListWidget, 6, 0, 1, 4)
        grid.addWidget(newAudioButton, 7, 0)
        grid.addWidget(saveButton, 7, 3)
        
        grid.setContentsMargins(0, 0, 0, 0)
        
        return self
    
    def languageSelectButtonClicked(self):
        self.audioListWidget.stopAllAudio()
        self.selectItem.emit()
        
    def newAudioButtonClicked(self):
        if self.current_rowid == None:
            reply = QMessageBox.question(self, 'Save first', 'Please save the item first. Save now?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.saveButtonClicked()
                self.audioListWidget.setRowID(self.current_rowid)
                self.audioListWidget.appendNewAudio()
        else:
            self.audioListWidget.appendNewAudio()
    
    def saveButtonClicked(self):
        
        name = self.nameLine.text()
        word = self.wordLine.text()
        phonetical = self.phoneticalLine.text()
        translation = self.translationLine.text()
        audio_filenames = None
        
        if self.current_rowid == None:
            svg_filename = str(int(time.time())) + self.randomword(5) + ".svg"
            
            self.freehandDrawWidget.saveView(path.join(self.deckpath, svg_filename))
            
            self.dbAdapter.saveDeckItem(name, word, phonetical, translation, svg_filename)
            
            self.current_rowid = self.dbAdapter.getDeckItemRowID(name, word, phonetical,  translation, svg_filename)
            self.svg_filename = svg_filename
            
            self.audioListWidget.setRowID(self.current_rowid)
            
        else:
            self.freehandDrawWidget.saveView(path.join(self.deckpath, self.svg_filename))
            
            self.dbAdapter.updateDeckItem(self.current_rowid, name, word, phonetical, translation, self.svg_filename)
            
        self.audioListWidget.saveStateToDB(self.current_rowid)
        
        QMessageBox.information(self, "saved", "saved")
        
        # return to parent view:
        #self.selectItem.emit()
    
    def clearDrawViewButtonClicked(self):#
        reply = QMessageBox.question(self, 'Drop Drawing', "really?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clearDrawView()
    
    def clearDrawView(self):
        self.freehandDrawWidget.clearView()
    
    def importImage(self):
        if self.current_rowid == None:
            reply = QMessageBox.question(self, 'Save first', 'Please save the item first. Save now?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.saveButtonClicked()
                self.audioListWidget.setRowID(self.current_rowid)
                
                self.importImageHelper()
        else:
            self.importImageHelper()
    
    def importImageHelper(self):
        file_path = QFileDialog.getOpenFileName(self, 'Please select an Image File', self.default_import_path)
        self.default_import_path = file_path[0]
        if file_path[0]:
            filename = file_path[0].split(sep)[::-1][0]
            target_path = path.join(self.deckpath, filename)
            shutil.copyfile(file_path[0], target_path)
            
            self.dbAdapter.insertImage(self.current_rowid, filename)
            
            self.initializeWithRowID(self.current_rowid)
    
    def deleteImage(self):
        if self.current_rowid and 'image' in self.dataset and self.dataset['image']:
            reply = QMessageBox.question(self, 'Delete Image', "really?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                remove_path = path.join(self.deckpath, self.dataset['image'])
                if path.exists(remove_path):
                    remove(remove_path)
                self.dbAdapter.deleteImage(self.current_rowid)
                self.dataset.pop('image')
                
                self.imageView.clear()
    
    def randomword(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    
