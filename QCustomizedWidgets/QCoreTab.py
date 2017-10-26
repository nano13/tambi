
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal

from QCustomizedWidgets.QCliWidget import QCliWidget
from modules.sword.QGui.QParallelBibleWidget import QParallelBibleWidget
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QMusicBeamerWidget import QMusicBeamerWidget

from misc.unicodeFonts import UnicodeFonts

class QCoreTab(QWidget):
    
    set_tab_text = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    """ just forward this signal """
    def setTabText(text):
        self.set_tab_text.emit(text)
    
    def cliTab(self):
        cli = QCliWidget()
        cli.set_tab_text.connect(self.setTabText)
        return cli
    
    def dualCliTab(self):
        layout = QHBoxLayout()
        layout.addWidget(QCliWidget())
        layout.addWidget(QCliWidget())
        self.setLayout(layout)
        
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
    
