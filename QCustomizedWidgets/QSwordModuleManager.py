
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QVBoxLayout
from PyQt5.QtCore import Qt

from modules.sword.sword_module_manager import SwordModuleManager

class QSwordModuleManager(QWidget):
    
    module_manager = SwordModuleManager()
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        #self.addTreeWidgetExample()
        self.addTreeWidget()
    
    def addTreeWidget(self):
        self.tree = QTreeWidget()
        self.tree.itemExpanded.connect(self.expanded)
        self.tree.itemSelectionChanged.connect(self.itemSelectionChanged)
        self.layout.addWidget(self.tree)
        self.tree.setColumnCount(2)
        
        self.addRemoteModules()
        self.addInstalledModules()
    
    def addRemoteModules(self):
        #data = self.prepareRemoteData()
        data = self.module_manager.listRemoteModules()
        
        for repo_name in data:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, repo_name)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            for language in sorted(data[repo_name]):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                child.setText(0, language)
                
                for module in data[repo_name][language]:
                    grandchild = QTreeWidgetItem(child)
                    grandchild.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    grandchild.setText(0, module['name'])
                    grandchild.setText(1, module['description'])
                    grandchild.setCheckState(0, Qt.Unchecked)
        
        
    def addInstalledModules(self):
        #data = self.prepareLocalData()
        data = self.module_manager.listLocalModules()
        
        #for repo_name in data[0]:
        #repo = sorted(data[0][repo_name])
        repo = sorted(data)
        
        parent = QTreeWidgetItem(self.tree)
        parent.setText(0, "Installed")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        
        for language in repo:
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child.setText(0, language)
            #child.setCheckState(0, Qt.Checked)
            
            #for i, module in enumerate(data[0]['installed'][language]):
            for module in data[language]:
                grandchild = QTreeWidgetItem(child)
                grandchild.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                grandchild.setText(0, module['name'])
                grandchild.setText(1, module['description'])
                grandchild.setCheckState(0, Qt.Checked)
                    
        self.tree.resizeColumnToContents(0)
        
    def itemSelectionChanged(self):
        print(self.tree.selectedItems())
        
    def expanded(self):
        self.tree.resizeColumnToContents(0)
    
    def addTreeWidgetExample(self):
        self.tree = QTreeWidget()
        self.layout.addWidget(self.tree)
        
        self.tree.setColumnCount(1)
        
        for i in range(3):
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, "Parent {}".format(i))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            for x in range(5):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                child.setText(0, "Child {}".format(x))
                child.setCheckState(0, Qt.Unchecked)
                
                for y in range(7):
                    grandchild = QTreeWidgetItem(child)
                    grandchild.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    grandchild.setText(0, "GrandChild {}".format(y))
                    grandchild.setCheckState(0, Qt.Unchecked)
            
