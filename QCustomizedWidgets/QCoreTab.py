
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal

from QCustomizedWidgets.QCliWidget import QCliWidget

from modules.vocable.QGui.QVocableStackedWidget import QVocableStackedWidget
from modules.musicbeamer.QMusicBeamerWidget import QMusicBeamerWidget

from misc.unicodeFonts import UnicodeFonts

from functools import partial

class QCoreTab(QWidget):
    
    set_tab_text = pyqtSignal(str)
    dual_cli_label = {'left': '', 'right': ''}
    
    def __init__(self):
        super().__init__()
    
    """ just forward this signal """
    def setTabText(self, text):
        self.set_tab_text.emit(text)
    
    def setDualTabText(self, position, text):
        self.dual_cli_label[position] = text
        
        label = self.dual_cli_label['left'] + ' | ' + self.dual_cli_label['right']
        self.set_tab_text.emit(label)
    
    def cliTab(self):
        cli = QCliWidget()
        cli.set_tab_text.connect(self.setTabText)
        return cli
    
    def dualCliTab(self):
        cli_left = QCliWidget()
        cli_right = QCliWidget()
        
        layout = QHBoxLayout()
        layout.addWidget(cli_left)
        layout.addWidget(cli_right)
        self.setLayout(layout)
        
        cli_left.set_tab_text.connect(partial(self.setDualTabText, 'left'))
        cli_right.set_tab_text.connect(partial(self.setDualTabText, 'right'))
        
        return self
    
    def editorTab(self, filepath):
        editor = QTextEdit()
        
        data = ""
        with open(filepath[0]) as fobj:
            for line in fobj:
                data += line
        
        unicode_fonts = UnicodeFonts()
        unicode_fonts.applyFontAndSizeToQWidget(data, editor)
        editor.setText(data)
        
        return editor
    
    def vocableTab(self):
        vocable_page = QVocableStackedWidget().vocableWidget()
        return vocable_page
    
    def musicBeamerTab(self):
        music_beamer_widget = QMusicBeamerWidget()
        return music_beamer_widget
    
