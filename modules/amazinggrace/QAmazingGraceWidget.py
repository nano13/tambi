
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

from QCustomizedWidgets.QBeamerWindow import QBeamerWindow

from functools import partial

class QAmazingGraceWidget(QWidget):
    
    beamer = None
    
    def __init__(self):
        super().__init__()
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        import os
        base, dirs, files = next(iter(os.walk('./modules/amazinggrace/data')))
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
    
    def amazingGraceButtonClicked(self, language):
        if not self.beamer == None:
            self.beamer.destroy()
        
        text = ''
        with open('./modules/amazinggrace/data/'+str(language)+'.tex', 'r') as fobj:
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
