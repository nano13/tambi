
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTextEdit

from QCustomizedWidgets.QCliTab import QCliTab
from QCustomizedWidgets.QVocableStackedWidget import QVocableStackedWidget
from QCustomizedWidgets.QMusicBeamerWidget import QMusicBeamerWidget

from functools import partial

from QCustomizedWidgets.QBeamerWindow import QBeamerWindow

class QCoreTab(QWidget):
    
    beamer = None
    
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
        grid = QGridLayout()
        self.setLayout(grid)
        
        import os
        base, dirs, files = next(iter(os.walk('./amazing_grace')))
        max_i = 0
        for i, f in enumerate(sorted(files)):
            label = str(f.split('.')[0])
            button = QPushButton(label)
            if i < len(files)/2:
                grid.addWidget(button, i, 0)
            else:
                grid.addWidget(button, i-len(files)/2, 1)
            button.clicked.connect(partial(self.amazingGraceButtonClicked, label))
            max_i += 1
            
        blank = QPushButton('blank')
        grid.addWidget(blank, max_i, 0, 1, 2)
        blank.clicked.connect(self.beamerCanvasBlank)
        return self
    def amazingGraceButtonClicked(self, language):
        if not self.beamer == None:
            self.beamer.destroy()
        
        text = ''
        with open('./amazing_grace/'+str(language)+'.tex', 'r') as fobj:
            for line in fobj:
                text += line.replace('\\\\', '')
        
        canvas = QBeamerWindow()
        canvas.setText(text)
        canvas.routeToScreen()
        self.beamer = canvas
        canvas.showFullScreen()
    def beamerCanvasBlank(self):
        if not self.beamer == None:
            self.beamer.destroy()
    
