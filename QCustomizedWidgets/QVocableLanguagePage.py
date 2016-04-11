
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from functools import partial

class QVocableLanguagePage(QWidget):
    def __init__(self):
        super().__init__()
        
    def vocableLanguagePage(self):
        grid = QGridLayout()
        layout = self.setLayout(grid)
        
        label_list = ["akkadian", "aramaic", "greek", "hebrew"]
        button_list = []
        for i, label in enumerate(label_list):
            button = QPushButton(label, self)
            button_list.append(button)
            
            grid.addWidget(button_list[i], i, 0)
            button_list[i].clicked.connect(partial(self.buttonClicked, label))
            #button_list[i].clicked.connect(lambda i=i: self.buttonClicked(i))
        
        return self
    
    def buttonClicked(self, label):
        print(label)
