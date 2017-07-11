
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTextEdit, QComboBox

from QCustomizedWidgets.QInputLine import QInputLine

from interpreter.interpreter import Interpreter

class QParallelBibleWidget(QWidget):
    
    interpreter = Interpreter()
    
    current_sword_module = None
    modules_list = ['GerNeUe', 'TR', 'GerSch']
    display_widgets_list = []
    
    modules_dropdown_list = []
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.display_widget = QDisplayWidget()
        self.display_widget.setDropdownItems(self.getModulesForDropdown())
        self.layout.addWidget(self.display_widget)
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        self.layout.addWidget(line)
        
    def commandEntered(self, command):
        """ store the originally selected sword module """
        self.current_sword_module = self.interpreter.interpreter('sword.getModule')
        
        for i, module in enumerate(self.modules_list):
            
            try:
                self.interpreter.interpreter('sword.setModule '+module)
                
                result = self.interpreter.interpreter(command)
            except ClearCalled:
                self.clearDisplayWidget()
            else:
                print(result.toString())
                self.display_widgets_list[i].setText(result)
        
        """ restore the originally seletectd sword module """
        self.interpreter.interpreter('sword.setModule '+module)
    
    def clearDisplayWidget(self):
        pass
    
    def getModulesForDropdown(self):
        result = self.interpreter.interpreter('sword.modules')
        
        print(result.payload[0])
        self.modules_dropdown_list = result

class QDisplayWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.dropdown = QComboBox()
        #self.dropdown.insertItems(0, ['a', 'b'])
        self.layout.addWidget(self.dropdown)
        
        self.display_widget = QTextEdit()
        self.layout.addWidget(self.display_widget)
    
    def setDropdownItems(self, items):
        self.dropdown.insertItems(0, items)
    
    def setText(self, text):
        self.display_widget.setText(text)
    
