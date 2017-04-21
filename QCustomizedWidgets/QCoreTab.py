
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTextEdit

from QCustomizedWidgets.QCliTab import QCliTab
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QMusicBeamerWidget import QMusicBeamerWidget
from QCustomizedWidgets.QAmazingGraceWidget import QAmazingGraceWidget

class QCoreTab(QWidget):
    
    
    def __init__(self):
        super().__init__()
        
    def cliTab(self):
        cli = QCliTab()
        return cli
        
    def editorTab(self, filepath):
        editor = QTextEdit()
        
        data = ""
        with open(filepath[0]) as fobj:
            for line in fobj:
                data += line
        
        self.unicode_fonts.applyFontAndSizeToQWidget(data, editor)
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
    
    
