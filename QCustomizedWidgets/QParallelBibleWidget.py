
from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit

from QCustomizedWidgets.QInputLine import QInputLine

from interpreter.interpreter import Interpreter

class QParallelBibleWidget(QWidget):
    
    interpreter = Interpreter()
    
    def __init__(self):
        super().__init__()
        
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        
        self.display_widget = QTextEdit()
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        self.grid.addWidget(line, 1, 0)
        
    def commandEntered(self, command):
        try:
            result = self.interpreter.interpreter(command)
        except ClearCalled:
            self.clearDisplayWidget()
        else:
            print(result.toString())
            
    def clearDisplayWidget(self):
        pass
