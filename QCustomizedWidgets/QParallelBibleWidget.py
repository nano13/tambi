
from PyQt5.QtWidgets import QWidget, QLayout, QVBoxLayout, QGridLayout, QTextEdit, QComboBox, QPushButton
from PyQt5.QtGui import QIcon

from QCustomizedWidgets.QInputLine import QInputLine

from interpreter.interpreter import Interpreter

class QParallelBibleWidget(QWidget):
    
    interpreter = Interpreter()
    
    current_sword_module = None
    #modules_list = ['GerNeUe', 'TR', 'GerSch']
    display_widgets_list = []
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        modules_dropdown_list = self.getModulesForDropdown()
        for i in range(0, 3):
            display_widget = QDisplayWidget()
            display_widget.setDropdownItems(modules_dropdown_list)
            self.display_widgets_list.append(display_widget)
            self.layout.addWidget(display_widget)
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        self.layout.addWidget(line)
        
    def commandEntered(self, command):
        """ store the originally selected sword module """
        self.current_sword_module = self.interpreter.interpreter('sword.getModule').payload
        
        for i, widget in enumerate(self.display_widgets_list):
            
            try:
                self.interpreter.interpreter('sword.setModule '+widget.getModuleName())
                
                result = self.interpreter.interpreter(command)
            except ClearCalled:
                self.clearDisplayWidget()
            else:
                print(result.toString())
                widget.setText(result.toString())
        
        """ restore the originally seletectd sword module """
        self.interpreter.interpreter('sword.setModule '+self.current_sword_module)
    
    def clearDisplayWidget(self):
        pass
    
    def getModulesForDropdown(self):
        result = self.interpreter.interpreter('sword.modules')
        
        modules = []
        for module in result.payload:
            modules.append(module[0])
        
        return sorted(modules)
    
class QDisplayLayout(QLayout):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
    

class QDisplayWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.dropdown = QComboBox()
        self.dropdown.currentIndexChanged.connect(self.comboBoxChanged)
        self.layout.addWidget(self.dropdown, 0, 0)
        
        new_language_button = QPushButton(self)
        new_language_button.setIcon(QIcon.fromTheme('window-new'))
        new_language_button.setMaximumSize(25, 20)
        new_language_button.clicked.connect(self.newLanguageButtonClick)
        self.layout.addWidget(new_language_button, 0, 1)
        
        close_language_button = QPushButton(self)
        close_language_button.setIcon(QIcon.fromTheme('window-close'))
        close_language_button.setMaximumSize(25, 20)
        close_language_button.clicked.connect(self.closeButtonClicked)
        self.layout.addWidget(close_language_button, 0, 2)
        
        self.display_widget = QTextEdit()
        self.display_widget.setReadOnly(True)
        self.layout.addWidget(self.display_widget, 1, 0, 3, 0)
    
    def setDropdownItems(self, items):
        self.dropdown.insertItems(0, items)
    
    def setText(self, text):
        self.display_widget.setText(text)
        
    def getModuleName(self):
        return self.dropdown.currentText()
        
    def comboBoxChanged(self, index):
        print(index)
        print(self.dropdown.currentText())
    
    def newLanguageButtonClick(self):
        pass
    
    def closeButtonClicked(self, button_id):
        print(button_id)
