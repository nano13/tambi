
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton, QTextEdit

from QCustomizedWidgets.QCliWidget import QCliWidget
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QMusicBeamerWidget import QMusicBeamerWidget
from QCustomizedWidgets.QAmazingGraceWidget import QAmazingGraceWidget

from misc.unicodeFonts import UnicodeFonts

class QCoreTab(QWidget):
    
    def __init__(self):
        super().__init__()
        
    def cliTab(self):
        cli = QCliWidget()
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
    
    def amazingGraceTab(self):
        amazing = QAmazingGraceWidget()
        return amazing
    
    
