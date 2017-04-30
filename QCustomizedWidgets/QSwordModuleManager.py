
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QVBoxLayout
from PyQt5.QtCore import Qt

from modules.sword.sword_module_manager import SwordModuleManager

class QSwordModuleManager(QWidget):
    
    module_manager = SwordModuleManager()
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.addTreeWidget()
    
    def addTreeWidget(self):
        self.tree = QTreeWidget()
        self.tree.itemExpanded.connect(self.expanded)
        self.tree.itemSelectionChanged.connect(self.itemSelectionChanged)
        self.layout.addWidget(self.tree)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['module', 'description'])
        
        data = self.module_manager.getAllModules()
        #print(data)
        
        self.addRemoteModules(data)
    
    def addRemoteModules(self, data):
        for repo_name in sorted(data):
            parent = QTreeWidgetItem(self.tree)
            if repo_name is not 'local':
                parent.setText(0, repo_name)
            else:
                parent.setText(0, 'Installed')
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            for language in sorted(data[repo_name]['modules']):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                child.setText(0, language)
                
                for module in data[repo_name]['modules'][language]:
                    grandchild = QTreeWidgetItem(child)
                    grandchild.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    grandchild.setText(0, module['name'])
                    grandchild.setText(1, module['description'])
                    if repo_name is not 'local':
                        grandchild.setCheckState(0, Qt.Unchecked)
                    else:
                        grandchild.setCheckState(0, Qt.Checked)
        self.tree.resizeColumnToContents(0)
    
    def itemSelectionChanged(self):
        print(self.tree.selectedItems())
    
    def expanded(self):
        self.tree.resizeColumnToContents(0)
    
